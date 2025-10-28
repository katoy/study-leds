#!/bin/bash

echo "=== バージョンファイル用 IPアドレス更新ツール ==="

# 現在のIPアドレスを取得
CURRENT_IP=$(ifconfig en0 | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}')

if [ -z "$CURRENT_IP" ]; then
    echo "❌ IPアドレスを検出できませんでした"
    exit 1
fi

echo "📡 検出されたIP: $CURRENT_IP"
echo ""

# 各バージョンファイルのIPアドレスを更新
for version_file in versions_*.json; do
    if [ -f "$version_file" ]; then
        echo "🔄 $version_file を更新中..."
        sed -i '' "s|http://[0-9.]*:8080|http://$CURRENT_IP:8080|g" "$version_file"
    fi
done

# config.pyも更新
if [ -f "config.py" ]; then
    echo "🔄 config.py を更新中..."
    sed -i '' "s/UPDATE_SERVER_IP = \"[0-9.]*\"/UPDATE_SERVER_IP = \"$CURRENT_IP\"/" config.py
fi

echo ""
echo "✅ 全ファイルをIP: $CURRENT_IP で更新しました"
echo ""
echo "📋 更新されたファイル:"
echo "   - versions_1.2.0.json"
echo "   - versions_2.0.0.json"
echo "   - versions_2.1.0.json"
echo "   - versions_2.2.0.json"
echo "   - config.py"
echo ""
echo "💡 次に実行: ./switch_version.sh で versions.json を更新してください"