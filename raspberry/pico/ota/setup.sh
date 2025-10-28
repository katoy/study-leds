#!/bin/bash

echo "=== Raspberry Pi Pico OTA セットアップ ==="
echo ""

# config.pyが存在するかチェック
if [ -f "config.py" ]; then
    echo "✅ config.py はすでに存在しています"
else
    echo "📝 テンプレートから config.py を作成中..."
    cp config.py.sample config.py
    echo "✅ config.py.sample から config.py を作成しました"
    echo ""
    echo "⚠️  重要: config.py でWiFi設定を編集してください！"
    echo "   1. WiFi SSID とパスワードを設定"
    echo "   2. MacのIPアドレスを設定"
    echo ""
fi

# versions.jsonのデフォルト設定
if [ ! -f "versions.json" ]; then
    echo "📝 デフォルトバージョン (v2.1.0 - OTA対応) を設定中..."
    cp versions_2.1.0.json versions.json
    echo "✅ v2.1.0 (OTAライブラリ版) で versions.json を作成しました"
    echo ""
else
    echo "✅ versions.json はすでに存在しています"
fi

# IPアドレスを自動検出して提案
echo "🔍 MacのIPアドレスを検出中..."
./get_ip.sh

echo ""
echo "📋 次のステップ:"
echo "1. config.py でWiFi認証情報を編集"
echo "2. config.py でIPアドレスを更新"
echo "3. 実行: ./deploy.sh でOTA対応アプリをデプロイ"
echo "4. 実行: python3 http_server.py でOTAサーバーを起動"
echo ""
echo "💡 デフォルトバージョン: v2.1.0 (0.5秒間隔 + OTAライブラリ)"
echo "   自動更新の準備完了！バージョン変更は ./switch_version.sh で"
echo ""
echo "🧩 利用可能なバージョン:"
echo "   - オプション 1: v1.2.0 (基本版・1秒間隔)"
echo "   - オプション 2: v2.0.0 (基本版・0.5秒間隔)"
echo "   - オプション 3: v2.1.0 (0.5秒間隔 + OTAライブラリ) ← 現在のデフォルト"
echo "   - オプション 4: v2.2.0 (1秒間隔 + OTAライブラリ)"
echo ""
echo "📖 詳細な手順は README.md または QUICKSTART.md をご覧ください"