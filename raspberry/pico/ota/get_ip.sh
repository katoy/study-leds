#!/bin/bash

echo "=== Mac IPアドレス検出 ==="
echo ""

# Wi-Fi接続のIPアドレスを取得
WIFI_IP=$(ipconfig getifaddr en0 2>/dev/null)
if [ -n "$WIFI_IP" ]; then
    echo "Wi-Fi (en0): $WIFI_IP"
    echo "  -> config.py で使用: UPDATE_SERVER_IP = \"$WIFI_IP\""
    echo "  -> versions.json で使用: \"url\": \"http://$WIFI_IP:8080/main.py\""
    echo ""
fi

# 有線接続のIPアドレスを取得
ETHERNET_IP=$(ipconfig getifaddr en1 2>/dev/null)
if [ -n "$ETHERNET_IP" ]; then
    echo "有線接続 (en1): $ETHERNET_IP"
    echo "  -> config.py で使用: UPDATE_SERVER_IP = \"$ETHERNET_IP\""
    echo "  -> versions.json で使用: \"url\": \"http://$ETHERNET_IP:8080/main.py\""
    echo ""
fi

# 詳細情報を表示
echo "=== 詳細ネットワーク情報 ==="
ifconfig | grep -E "^(en0|en1)" -A 5 | grep -E "(en0|en1|inet )"

echo ""
echo "=== クイックセットアップコマンド ==="
if [ -n "$WIFI_IP" ]; then
    echo "# Wi-Fi IPで config.py を更新:"
    echo "sed -i '' 's/UPDATE_SERVER_IP = \".*\"/UPDATE_SERVER_IP = \"$WIFI_IP\"/' config.py"
    echo ""
    echo "# Wi-Fi IPで versions.json を更新:"
    echo "sed -i '' 's|http://[0-9.]*:8080|http://$WIFI_IP:8080|g' versions.json"
    echo "sed -i '' 's|http://[0-9.]*:8080|http://$WIFI_IP:8080|g' versions_v2.json"
fi