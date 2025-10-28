#!/bin/bash

echo "=== バージョン切り替えツール ==="
echo ""
echo "現在のバージョン:"
cat versions.json | grep version

echo ""
echo "利用可能なバージョン:"
echo "1) v1.1.0 (0.2秒間隔 - 基本版)"
echo "2) v1.2.0 (1秒間隔 - 基本版)"
echo "3) v2.1.0 (0.2秒間隔 + OTAライブラリ - デフォルト)"
echo "4) v2.2.0 (1秒間隔 + OTAライブラリ)"
echo ""

read -p "バージョンを選択 (1-4): " choice


case $choice in
    1)
        echo "v1.1.0 (0.2秒間隔 - 基本版) に切り替え中..."
        cp versions_1.1.0.json versions.json
        ;;
    2)
        echo "v1.2.0 (1秒間隔 - 基本版) に切り替え中..."
        cp versions_1.2.0.json versions.json
        ;;
    3)
        echo "v2.1.0 (OTAライブラリ - 0.2秒) に切り替え中..."
        cp versions_2.1.0.json versions.json
        ;;
    4)
        echo "v2.2.0 (OTAライブラリ - 1秒) に切り替え中..."
        cp versions_2.2.0.json versions.json
        ;;
    *)
        echo "❌ 無効な選択です。1-4を選択してください。"
        exit 1
        ;;
esac

echo ""
echo "新しいバージョン設定:"
cat versions.json
