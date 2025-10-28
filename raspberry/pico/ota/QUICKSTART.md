### ログファイルについて

- Pico上では `boot_error.log` などのログファイルが自動生成されます。
- ログは `lib/ota/log_helper.py` の append_debug により、時刻付きで追記されます。
- ログファイルはデフォルトで16KBを超えると古い行から自動的に削除されます（ファイル肥大化防止）。
- エラーやOTAの詳細な動作記録を確認したい場合は、Pico内のログファイルを参照してください。
# 🚀 クイックスタートガイド

## 1. 基本セットアップ（3分）

### 必要なもの
- Raspberry Pi Pico W
- Mac（このプロジェクトが入っているMac）
- 同じWi-Fiネットワーク

### 自動セットアップ（推奨）
```bash
./setup.sh
```

このスクリプトは：
- `config.py`を作成
- **デフォルトでv2.1.0を設定**（OTA機能付き・推奨版／0.2秒間隔）
- IPアドレスを自動検出

### WiFi設定
セットアップ後、`config.py`を開いてWiFi設定を変更：
```python
WIFI_SSID = "your_wifi_name"      # ← あなたのWi-Fi名
WIFI_PASSWORD = "your_password"   # ← あなたのWi-Fiパスワード
UPDATE_SERVER_IP = "192.168.0.104"  # ← setup.shで表示されたIP
```

## 2. バージョン選択（オプション）

```bash
# 必要に応じてバージョンを変更
./switch_version.sh
```

**デフォルト**: v2.1.0 (0.2秒間隔 + OTAライブラリ) ← **そのまま使用推奨**

**その他の選択肢**:
- **1**: v1.1.0 (0.2秒間隔・基本版)
- **2**: v1.2.0 (1秒間隔・基本版)
- **3**: v2.1.0 (0.2秒間隔 + OTAライブラリ)
- **4**: v2.2.0 (1秒間隔 + OTAライブラリ)

## 3. 最初のデプロイ（2分）

```bash
# デバイスを接続してからこのコマンドを実行
./deploy.sh
```

## 4. OTA機能をテスト（3分）

### 方法A: OTA統合版を使用（推奨・簡単）

#### ステップ1: HTTPサーバー起動
```bash
python3 http_server.py
```

#### ステップ2: バージョン変更をテスト
```bash
# 別のバージョンに切り替え
./switch_version.sh
# → 違うバージョンを選択（例: 3→4 または 4→3）
```

**自動更新確認**: デバイスが定期的に更新をチェックし、新しいバージョンを自動ダウンロード＆適用します！

### 🧩 OTAライブラリ使用版の特徴

- **超簡単**: たった数行でOTA機能を追加
- **必須設定**: `config.py`が必須（設定不備時は日本語エラー表示）
- **確実な動作**: 設定ファイルがない場合は起動時にエラー終了
- **メモリ効率**: 必要な時だけWiFiを有効化
- **エラー処理**: ネットワークエラーを適切に処理

#### ファイル
- `main_v2_1_ota.py`: 0.2秒間隔 + OTAライブラリ (v2.1.0) ← **デフォルト**
- `main_v2_2_ota.py`: 1秒間隔 + OTAライブラリ (v2.2.0)
- `lib/ota/log_helper.py`: OTAロギングヘルパー
- `lib/ota/ota_manager.py`: OTAマネージャ本体
- `lib/ota/ota_enabled_app.py`: OTA対応アプリ基底クラス
- `ota_client.py`: 独立したOTAクライアント（config.py必須、日本語エラー対応）

### 方法B: 手動でのOTA検証

#### バージョン変更をテスト
```bash
# 現在のバージョンを確認
cat versions.json | grep version

# 別のバージョンに切り替え
./switch_version.sh

# デバイスが自動的に新しいバージョンを検出・更新
```

## 5. バージョンの切り替え・ダウングレード

### 任意のバージョンに切り替える方法

#### 方法1: バージョン切り替えスクリプト（最も簡単）
```bash
# インタラクティブなバージョン選択
./switch_version.sh

# 選択肢:
# 1) v1.1.0 (0.2秒間隔・基本版)
# 2) v1.2.0 (1秒間隔・基本版)
# 3) v2.1.0 (0.2秒間隔・OTA版) ← 推奨
# 4) v2.2.0 (1秒間隔・OTA版) ← 推奨
```

#### 方法2: 直接デプロイ（即座に反映）
```bash
# 任意のバージョンを選択
./switch_version.sh

# main_v1_1.pyやmain_v1_2.pyを直接デプロイ
./deploy.sh
```

#### 方法3: OTA経由で自動切り替え（OTA版のみ）
```bash
# Step 1: バージョンを変更
./switch_version.sh

# Step 2: デバイスが自動的に新バージョンを検出
# 約30秒後に自動更新される！
```

### バージョン確認
```bash
# 現在のバージョンを確認
cat versions.json | grep version

# シリアル出力を確認
mpremote connect /dev/cu.usbmodem1101 repl

# v1.1.0の場合: "200ms interval"
# v1.2.0の場合: "1000ms interval"
# v2.1.0の場合: "OTA library - 200ms interval"
# v2.2.0の場合: "OTA library - 1000ms interval"
```

## 6. IP設定の管理

### ネットワーク変更時
```bash
# 全バージョンファイルのIPを一括更新
./update_ip.sh

# バージョンを再選択してversions.jsonを更新
./switch_version.sh
```

## 7. サーバー側でのバージョン確認

### HTTPサーバーの動作確認
```bash
# HTTPサーバーを起動（まだ起動していない場合）
python3 http_server.py

# または、サーバー状態の詳細チェック
./check_server.sh
```

### ブラウザでバージョン確認
ブラウザで以下のURLにアクセス：
- **versions.json**: http://localhost:8080/versions.json
- **main_v1_1.py**: http://localhost:8080/main_v1_1.py
- **main_v1_2.py**: http://localhost:8080/main_v1_2.py

### コマンドラインでバージョン確認
```bash
# 現在配信中のバージョン情報を確認
curl http://localhost:8080/versions.json

# 期待される出力例（v1.2.0の場合）:
# {
#   "version": "1.2.0",
#   "files": [
#     {"name": "main_v1_1.py", "url": "http://192.168.0.104:8080/main_v1_1.py"}
#   ]
# }

# main_v1_1.pyファイルの内容を確認
curl http://localhost:8080/main_v1_1.py | head -10
```

### IPアドレス経由でのアクセス
```bash
# 他の端末からアクセスする場合
curl http://192.168.0.104:8080/versions.json

# またはブラウザで
# http://192.168.0.104:8080/versions.json
```

## 6. シリアル出力で確認

```bash
mpremote connect /dev/cu.usbmodem1101 repl
```

## 🎯 期待される動作

### v1.1.0の動作
- LED が0.2秒間隔で点滅
- 点滅回数のカウンター表示
- 10秒ごとの点滅数レポート
- シリアル出力: "Simple LED Controller v1.1.0"

### v1.2.0の動作
- LED が1秒間隔で点滅
- 点滅回数のカウンター表示
- 10秒ごとの点滅数レポート
- シリアル出力: "Simple LED Controller v1.2.0"

## 🔧 トラブルシューティング

### サーバー関連の問題

1. **HTTPサーバーが起動しない**
   ```bash
   # ポート8080が使用中かチェック
   lsof -i :8080

   # サーバー状態をチェック
   ./check_server.sh
   ```

2. **versions.jsonにアクセスできない**
   ```bash
   # ローカルでテスト
   curl http://localhost:8080/versions.json

   # ブラウザでアクセス
   open http://localhost:8080/versions.json
   ```

3. **外部からアクセスできない**
   ```bash
   # IPアドレスを確認
   ./get_ip.sh

   # ファイアウォール設定を確認
   # システム環境設定 > セキュリティとプライバシー > ファイアウォール
   ```

### よくある問題

1. **デバイスが見つからない**
   ```bash
   ls /dev/cu.usbmodem*
   ```

2. **WiFi接続失敗**
   - config.pyのSSID/パスワードを確認
   - MacとPico Wが同じネットワークにいるか確認
   - config.pyが存在しない場合は日本語エラーメッセージが表示されます

3. **OTA更新されない**
   - http_server.pyが起動しているか確認
   - versions.jsonのIPアドレスが正しいか確認
   - config.pyの設定が最新かチェック
   - config.pyが不足している場合は起動時にエラー終了します

### IP設定の確認・更新
```bash
./get_ip.sh       # 現在のIPを確認
./update_ip.sh    # 全ファイルのIPを一括更新
```

---

## 🎯 新ワークフロー完全ガイド

### 🚀 初回セットアップ
```bash
./setup.sh                    # 基本設定（自動でv2.1.0設定）
# ./switch_version.sh         # 必要に応じてバージョン変更
./deploy.sh                   # デプロイ
python3 http_server.py        # OTAサーバー起動
```

### 🔄 バージョン変更
```bash
./switch_version.sh           # 新しいバージョンを選択
# OTA版なら自動更新、基本版なら ./deploy.sh
```

### 🌐 ネットワーク変更時
```bash
./update_ip.sh               # 全ファイルのIP更新
./switch_version.sh          # versions.json再生成
```

### ✨ おすすめ設定
- **v2.1.0** (0.5秒間隔 + OTAライブラリ) ← **デフォルト設定**
- **v2.2.0** (1秒間隔 + OTAライブラリ)

**これで完璧なOTAシステムの完成です！** 🎉

## 📱 実用例

このシステムは以下のような用途に使えます：

- **IoTデバイスの遠隔更新**
- **センサーデータの収集システム**
- **スマートホーム機器の制御**
- **プロトタイプの継続的な改善**

## 🔧 設定ファイル管理

### config.py必須設定システム
すべてのOTAクライアント（`lib/ota/ota_enabled_app.py`、`ota_client.py`、OTA統合版）は：
- **config.pyが必須**（設定ファイルがない場合はエラー終了）
- 設定不備時は**日本語エラーメッセージ**を表示
- 設定ファイル作成手順を自動ガイド
- ネットワーク変更時も`config.py`を更新するだけで対応

### エラーメッセージ例
```
エラー: config.py が見つかりません！
WIFI_SSID、WIFI_PASSWORD、UPDATE_SERVER_IP を含む config.py を作成してください
例: cp config.py.sample config.py
```

---
**重要**: **config.pyは必須ファイルです**。初回セットアップ時は必ず作成し、WiFi設定とIPアドレスを正しく設定してください。