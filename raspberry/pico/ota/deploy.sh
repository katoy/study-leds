#!/bin/bash
#


# Raspberry Pi Pico OTAデプロイメントスクリプト
#
# 【主な機能】
# - versions.json で指定された全ファイルをまとめてPicoに転送
# - ファイルごとにリモート側のディレクトリを自動作成（lib/ota など多階層も対応）
# - mpremote を使い、転送後にPicoを自動リセット
#
# 【使い方】
#   ./deploy.sh [デバイス] [ファイル]
#   例: ./deploy.sh /dev/cu.usbmodem1101
#   ※ versions.json が存在する場合は全ファイル一括デプロイ、なければ単一ファイルデプロイ
#
# 【注意点】
# - mpremote の "device busy" エラー時は他プロセス（Thonny, screen等）を終了し、デバイスを解放してください
# - OTAバージョン切り替えは switch_version.sh で versions.json を切り替えてから本スクリプトを実行
# - config.py など必須ファイルの存在・内容も事前に確認してください
#

DEVICE=${1:-"/dev/cu.usbmodem1101"}
DEST_FILE=${2:-"main.py"}  # 転送先ファイル名

echo "=== Raspberry Pi Pico OTA デプロイメント ==="
echo "デバイス: $DEVICE"

# 現在のバージョンと転送元ファイル情報を取得
VERSION="不明"
DEPLOY_ALL=false

if [ -f "versions.json" ]; then
    VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' versions.json | cut -d'"' -f4)
    echo "バージョン: $VERSION"
    echo ""

    # versions.jsonからすべてのファイル情報を取得
    echo "📋 デプロイ対象ファイル:"
    python3 - <<'PY' > /tmp/deploy_files.txt
import json
try:
    with open('versions.json') as f:
        data = json.load(f)
    for file_info in data['files']:
        # derive source path relative to repo: use the path part of the URL after host
        url = file_info['url']
        path_after_host = url.split('://')[-1].split('/',1)[-1]
        source = path_after_host
        dest = file_info['name']
        print(f'  {source} → {dest}')
        print(f'{source}|{dest}')
except Exception as e:
    print(f'Error: {e}')
PY

    # エラーメッセージを除外して、ファイルマッピングのみを表示
    grep -v "Error:" /tmp/deploy_files.txt | grep -v "→" || true
    grep "→" /tmp/deploy_files.txt || true

    DEPLOY_ALL=true
else
    echo "ファイル: $DEST_FILE"
    echo "警告: versions.json が見つかりません"
    DEPLOY_ALL=false
fi

# デバイスが接続されているかチェック
if [ ! -e "$DEVICE" ]; then
    echo "エラー: デバイス $DEVICE が見つかりません"
    echo "利用可能なデバイス:"
    ls /dev/cu.usbmodem* 2>/dev/null || echo "USBデバイスが見つかりません"
    exit 1
fi

if [ "$DEPLOY_ALL" = true ]; then
    echo ""
    echo "🚀 全ファイルデプロイを開始..."

    # 2. versions.jsonからファイルを順次デプロイ
    python3 - <<'PY' | while IFS='|' read -r source_file dest_file; do
import json, sys
try:
    with open('versions.json') as f:
        data = json.load(f)
    for file_info in data['files']:
        url = file_info['url']
        path_after_host = url.split('://')[-1].split('/',1)[-1]
        source = path_after_host
        dest = file_info['name']
        print(f'{source}|{dest}')
except Exception:
    sys.exit(1)
PY
        if [ -f "$source_file" ]; then
            echo "📁 デプロイ中: $source_file → $dest_file"
            # リモートに親ディレクトリがなければ作成（mpremote の cp は中間ディレクトリを自動作成しない）
            dir=$(dirname "$dest_file")
            if [ "$dir" != "." ]; then
                # 階層ごとに mkdir (lib/ota なら lib → lib/ota の順)
                IFS='/' read -ra PARTS <<< "$dir"
                path=""
                for part in "${PARTS[@]}"; do
                    if [ -z "$path" ]; then
                        path="$part"
                    else
                        path="$path/$part"
                    fi
                    echo "   📁 リモートにディレクトリ作成: $path"
                    mpremote connect "$DEVICE" fs mkdir ":$path" || true
                done
            fi
            mpremote connect "$DEVICE" fs cp "$source_file" ":$dest_file"
            if [ $? -eq 0 ]; then
                echo "   ✅ 成功: $dest_file"
            else
                echo "   ❌ 失敗: $dest_file"
                exit 1
            fi
        else
            echo "   ⚠️  スキップ: $source_file が見つかりません"
        fi
    done



    echo ""
    echo "✅ 全ファイルデプロイメント成功！"
    echo "📦 デプロイ済みバージョン: $VERSION"
    echo "デバイスをリセット中..."
    mpremote connect "$DEVICE" reset
    echo "✅ デバイスリセット完了"

else
    # 単一ファイルデプロイ（従来の動作）
    if [ ! -f "$FILE" ]; then
        echo "エラー: ファイル $FILE が見つかりません"
        exit 1
    fi

    echo "$FILE → $DEST_FILE をデバイスにデプロイ中..."
    mpremote connect "$DEVICE" fs cp "$FILE" ":$DEST_FILE"

    if [ $? -eq 0 ]; then
        echo "✅ デプロイメント成功！"
        echo "デバイスをリセット中..."
        sleep 2
        mpremote connect "$DEVICE" reset
        echo "✅ デバイスリセット完了"
    else
        echo "❌ デプロイメント失敗"
        exit 1
    fi
fi