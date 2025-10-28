#!/bin/bash

echo "=== OTAサーバー状態チェック ==="
echo ""

# サーバーが起動しているかチェック
echo "🔍 HTTPサーバーの稼働状況を確認中..."
if curl -s http://localhost:8080/versions.json > /dev/null 2>&1; then
    echo "✅ HTTPサーバーがポート8080で稼働中"
else
    echo "❌ HTTPサーバーが稼働していません"
    echo "💡 サーバー起動: python3 http_server.py"
    exit 1
fi

echo ""
echo "📋 現在のバージョン設定:"
curl -s http://localhost:8080/versions.json | python3 -m json.tool

echo ""
echo "🌐 利用可能なエンドポイント:"
echo "- バージョン: http://localhost:8080/versions.json"
echo "- メイン v1.2.0: http://localhost:8080/main.py"
echo "- メイン v2.0.0: http://localhost:8080/main_v2.py"

echo ""
echo "🔗 外部アクセス (IPアドレスを置き換えてください):"
IP=$(ipconfig getifaddr en0 2>/dev/null)
if [ -n "$IP" ]; then
    echo "- バージョン: http://$IP:8080/versions.json"
    echo "- Pico W から: このIPをconfig.pyで使用"
else
    echo "- IPアドレス確認: ./get_ip.sh を実行"
fi

echo ""
echo "⚡ クイックアクション:"
echo "- バージョン切り替え: ./switch_version.sh"
echo "- Picoへデプロイ: ./deploy.sh"
echo "- IP取得: ./get_ip.sh"