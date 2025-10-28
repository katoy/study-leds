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

echo "=== Raspberry Pi Pico OTA デプロイメント ==="
echo "デバイス: $DEVICE"

DEVICE=${1:-"/dev/cu.usbmodem1101"}
TARGET_FILE=${2:-"main.py"}

echo "=== Raspberry Pi Pico OTA デプロイメント ==="
echo "デバイス: $DEVICE"

# 共通: エラー時即終了
set -e

# デバイス存在チェック
if [ ! -e "$DEVICE" ]; then
    echo "エラー: デバイス $DEVICE が見つかりません"
    ls /dev/cu.usbmodem* 2>/dev/null || echo "USBデバイスが見つかりません"
    exit 1
fi

# versions.jsonからファイルリスト取得
get_file_list() {
    python3 - <<'PY'
import json
try:
    with open('versions.json') as f:
        data = json.load(f)
    for file_info in data['files']:
        url = file_info['url']
        path_after_host = url.split('://')[-1].split('/',1)[-1]
        source = path_after_host
        dest = file_info['name']
        print(f'{source}|{dest}')
except Exception as e:
    exit(1)
PY
}

# 階層ディレクトリ作成
ensure_remote_dirs() {
    local dest_file="$1"
    local dir=$(dirname "$dest_file")
    if [ "$dir" = "." ]; then return; fi
    IFS='/' read -ra PARTS <<< "$dir"
    local path=""
    for part in "${PARTS[@]}"; do
        path=${path:+$path/}$part
        mpremote connect "$DEVICE" fs ls ":$path" >/dev/null 2>&1 || {
            echo "   📁 リモートにディレクトリ作成: $path"
            mpremote connect "$DEVICE" fs mkdir ":$path"
        }
    done
}

# ファイル転送
deploy_file() {
    local src="$1"
    local dst="$2"
    echo "📁 デプロイ中: $src → $dst"
    ensure_remote_dirs "$dst"
    mpremote connect "$DEVICE" fs cp "$src" ":$dst" 1>/dev/null && {
        echo "   ✅ 成功: $dst"
    } || {
        echo "   ❌ 失敗: $dst"
        echo "   エラー発生のためデプロイを中断します。"
        exit 1
    }
}

# 全ファイルデプロイ
if [ -f "versions.json" ]; then
    VERSION=$(grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' versions.json | cut -d'"' -f4)
    echo "バージョン: $VERSION"
    echo ""
    echo "🚀 全ファイルデプロイを開始..."
    get_file_list | while IFS='|' read -r src dst; do
        if [ -f "$src" ]; then
            deploy_file "$src" "$dst"
        else
            echo "   ⚠️  スキップ: $src が見つかりません"
        fi
    done
    echo ""
    echo "✅ 全ファイルデプロイメント成功！"
    echo "📦 デプロイ済みバージョン: $VERSION"
    echo "   ✍️  version.txt を作成中..."
    mpremote connect "$DEVICE" exec "with open('version.txt', 'w') as f: f.write('$VERSION')"
    echo "   ✅ version.txt 作成完了"
    echo "デバイスをリセット中..."
    mpremote connect "$DEVICE" reset || {
        echo "⚠️  デバイスリセットに失敗しました"; exit 1; }
    echo "✅ デバイスリセット完了"
else
    # 単一ファイルデプロイ
    if [ ! -f "$TARGET_FILE" ]; then
        echo "エラー: ファイル $TARGET_FILE が見つかりません"
        exit 1
    fi
    echo "$TARGET_FILE → $TARGET_FILE をデバイスにデプロイ中..."
    deploy_file "$TARGET_FILE" "$TARGET_FILE"
    echo "デバイスをリセット中..."
    mpremote connect "$DEVICE" reset || {
        echo "⚠️  デバイスリセットに失敗しました"; exit 1; }
    echo "✅ デバイスリセット完了"
fi
