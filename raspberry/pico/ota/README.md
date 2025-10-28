### ログファイルについて

- Pico上では `boot_error.log` などのログファイルが自動生成されます。
- ログは `lib/ota/log_helper.py` の append_debug により、時刻付きで追記されます。
- ログファイルはデフォルトで16KBを超えると古い行から自動的に削除されます（ファイル肥大化防止）。
- エラーやOTAの詳細な動作記録を確認したい場合は、Pico内のログファイルを参照してください。

## 🆕 2025/10: OTAの信頼性向上

- OTAマネージャ初期化時にWiFiインターフェースをソフト的に強制リセット（off/on）する仕様を追加。
- これにより、USB抜き差し不要でWiFi接続の安定性が向上。
- OTA対応アプリはmain.py等から個別にWiFiリセット処理を呼ぶ必要はありません。


# Raspberry Pi Pico W OTA（Over-The-Air）アップデートシステム

このプロジェクトは、Raspberry Pi Pico W向けのOTA（Over-The-Air）アップデート機能を提供します。WiFi経由でプログラムを自動更新できる包括的なシステムです。

## 📁 ファイル構成

```
ota/
├── README.md                # このファイル
├── QUICKSTART.md           # クイックスタートガイド
├── .gitignore              # Git除外設定
├── setup.sh                # 初期セットアップスクリプト
├── config.py.sample        # 設定ファイルのサンプル
├── boot.py                 # SD カード起動用（オプション）
├── main_v1_1.py           # メインアプリケーション v1.1.0（0.2秒間隔）
├── main_v1_2.py           # メインアプリケーション v1.2.0（1秒間隔）
├── main_v2_1_ota.py       # v2.1.0 OTA統合版（0.2秒間隔）
├── main_v2_2_ota.py       # v2.2.0 OTA統合版（1秒間隔）
├── lib/ota/log_helper.py  # OTAロギングヘルパー
├── lib/ota/ota_manager.py # OTAマネージャ本体
├── lib/ota/ota_enabled_app.py # OTA対応アプリ基底クラス
├── ota_client.py          # OTAクライアント（統合版）
├── ota_updater.py         # OTAアップデーター（シンプル版）
├── http_server.py         # Mac用HTTPサーバー
├── deploy.sh              # デプロイメントスクリプト
├── switch_version.sh      # バージョン切り替えスクリプト
├── update_ip.sh           # IP一括更新スクリプト
├── get_ip.sh              # IP確認スクリプト
├── versions.json          # 現在選択されているバージョン情報
├── versions_1.2.0.json    # v1.2.0 バージョン定義
├── versions_2.0.0.json    # v2.0.0 バージョン定義
├── versions_2.1.0.json    # v2.1.0 バージョン定義（OTA統合）
├── versions_2.2.0.json    # v2.2.0 バージョン定義（OTA統合）
├── led.py                 # シンプルLED例
└── led2.py               # シンプルLED例（2秒間隔）

# Gitで管理されないファイル（.gitignoreで除外）
├── config.py              # 個人の設定ファイル
└── version.txt            # ローカルバージョン情報

> **補足:** `main.py` はPico上で実行されるエントリポイントですが、OTAやdeploy.shで自動的に生成・転送されます。リポジトリ内に main.py を置く必要はありません。
```

## 🚀 セットアップ
> **注意:** `boot.py` は初回のみ手動でPicoに転送してください（OTAやdeploy.shでは自動転送されません）。
### 1. 必要なソフトウェア

Mac側：
```bash
# mpremoteのインストール
pip install mpremote

# Python 3.6以上が必要
python3 --version

### デプロイ仕様補足
- deploy.shはversions.jsonの内容に従い、必要な全ファイルをPicoに自動転送します。
- ファイルごとにリモートディレクトリを自動作成し、転送後にPicoを自動リセットします。
- mpremoteの"device busy"エラー時は他プロセスを終了し、USBを抜き差ししてください。
```

### 2. 初期セットアップ（推奨）

```bash
# 自動セットアップスクリプトを実行
./setup.sh
```

このスクリプトは以下を行います：
- `config.py.sample`から`config.py`を作成
- **デフォルトでv2.1.0（OTA版／0.2秒間隔）を設定**
- MacのIPアドレスを自動検出

### 3. バージョン選択（オプション）

```bash
# 必要に応じてバージョンを変更
./switch_version.sh
```

**デフォルト**: v2.1.0 (0.2秒間隔 + OTAライブラリ) ← **そのまま使用推奨**

利用可能なバージョン：
1. **v1.1.0**: 0.2秒間隔（基本版）
2. **v1.2.0**: 1秒間隔（基本版）
3. **v2.1.0**: 0.2秒間隔 + OTAライブラリ（**デフォルト**）
4. **v2.2.0**: 1秒間隔 + OTAライブラリ

### 4. IP設定の管理

ネットワークが変わった際は：

```bash
# 全バージョンファイルのIPを一括更新
./update_ip.sh

# バージョンを再選択してversions.jsonを更新
./switch_version.sh
```

### 5. 手動設定（上級者向け）

`config.py.sample`を`config.py`にコピーして編集：

```bash
cp config.py.sample config.py
```

`config.py` を編集して環境に合わせて設定：

```python
# WiFi設定
WIFI_SSID = "your_wifi_name"
WIFI_PASSWORD = "your_wifi_password"

# MacのIPアドレス（./get_ip.sh で確認）
UPDATE_SERVER_IP = "192.168.0.104"
```

### 6. MacのIPアドレス確認

```bash
# 自動検出スクリプトを使用（推奨）
./get_ip.sh

# または手動で確認
ifconfig en0 | grep inet
ipconfig getifaddr en0
```

## 🔧 使用方法

### 推奨ワークフロー

```bash
# 1. セットアップ（v2.1.0が自動設定される）
./setup.sh

# 2. バージョン選択（オプション）
# ./switch_version.sh

# 3. デプロイ
./deploy.sh

# 4. OTAサーバー起動
python3 http_server.py
```

### 方法1: 自動デプロイメント（推奨）

```bash
# デバイスを自動検出してmain_v1_1.pyやmain_v1_2.pyをデプロイ
./deploy.sh

# 特定のデバイスとファイルを指定
./deploy.sh /dev/cu.usbmodem1101 main_v1_1.py
```

### 方法2: 手動デプロイメント

```bash
# main_v1_1.pyをPico Wに転送
mpremote connect /dev/cu.usbmodem1101 fs cp main_v1_1.py :main.py

# デバイスをリセット
mpremote connect /dev/cu.usbmodem1101 reset
```

### 方法3: OTA統合版の使用（推奨）

```bash
# OTA統合版を選択してデプロイ（自動更新機能付き）
./switch_version.sh  # 3または4を選択
./deploy.sh
```

## 📡 OTAアップデート

### 1. HTTPサーバーを起動

Mac側でHTTPサーバーを起動：

```bash
python3 http_server.py
```

サーバー情報：
- ポート: 8080
- URL: http://localhost:8080
- バージョン情報: http://localhost:8080/versions.json

### 2. アップデートファイルの準備

新しいバージョンをアップデートする場合：

1. `versions.json` を編集してバージョン番号を更新
2. 新しい`main_v1_1.py`や`main_v1_2.py`ファイルを準備
3. HTTPサーバーが起動していることを確認

例（v1.2.0 → v2.0.0）：
```bash
# versions.jsonをv2.0.0用に置き換え
cp versions_v2.json versions.json

# サーバーを再起動
python3 http_server.py
```

### 3. OTA実行

Pico W側で自動的に更新がチェックされ、新しいバージョンがあれば自動的にダウンロード・適用されます。

## 🏗️ アプリケーション例

### 基本版（OTA機能なし）
- **main_v1_1.py (v1.1.0)**: 0.2秒間隔でのシンプルな点滅
- **main_v1_2.py (v1.2.0)**: 1秒間隔でのシンプルな点滅

### OTA統合版（推奨・デフォルト）
- **main_v2_1_ota.py (v2.1.0)**: 0.2秒間隔 + OTAライブラリ（**デフォルト**）
- **main_v2_2_ota.py (v2.2.0)**: 1秒間隔 + OTAライブラリ

#### OTA統合版の特徴
- 起動時に自動更新チェック
- 60秒間隔での定期更新チェック
- WiFi接続・切断の自動管理
- **config.py必須**（設定ファイルがない場合はエラー終了）
- 別途OTAクライアントが不要

### OTA単体クライアント（上級者向け）
- **ota_client.py**: 独立したOTAクライアント
- config.py必須（設定不備時は日本語エラーメッセージ表示）
- 設定ファイル作成手順を自動ガイド

## 🔍 トラブルシューティング

### デバイスが見つからない場合

```bash
# 利用可能なデバイスを確認
ls /dev/cu.usbmodem*

# mpremoteでデバイス確認
mpremote devs
```

### WiFi接続の問題

1. `config.py`のSSIDとパスワードを確認
2. MacとPico Wが同じネットワークにいることを確認
3. MacのIPアドレスが正しいことを確認

### OTA更新が動作しない場合

1. HTTPサーバーが起動していることを確認
2. `versions.json`のURLが正しいことを確認
3. ファイアウォール設定を確認

## 🆘 Picoのシリアルポートが認識されない場合の対処法

1. **USBケーブルを抜き差しする**
   - Pico WのUSBケーブルを一度抜き、数秒後に再接続してください。
   - Finderや`/dev/cu.usbmodem*`でデバイスが現れるか確認。

2. **他のアプリ（Thonny, screen等）をすべて終了**
   - 他のシリアル接続アプリがPicoを掴んでいるとポートが見えません。すべて終了し、再度USBを抜き差し。

3. **リカバリーモード（BOOTSEL）で起動**
   - BOOTSELボタンを押しながらUSB接続し、RPI-RP2ストレージとして認識されるか確認。
   - 認識された場合はファームウェアの再書き込みも可能です。

4. **Macの再起動**
   - OS側のデバイス認識不良時はMacを再起動。

5. **ケーブルやUSBポートの変更**
   - 別のUSBケーブルやポートを試してください。

6. **ファームウェアの再書き込み（強制初期化）**
   - [flash_nuke.uf2](https://datasheets.raspberrypi.com/soft/flash_nuke.uf2) をドラッグ＆ドロップしてフラッシュ全消去。
   - その後、Pico W（2Wの場合は `RPI_PICO2_W-20250911-v1.26.1.uf2` など）をドラッグ＆ドロップで書き込み。
   - これで多くの認識・起動トラブルが解消します。

上記でも解決しない場合は、Pico本体の故障やドライバの問題も考えられます。

## 🆘 OTA更新後にアプリが起動しない・動作しない場合の対処法

0. **Picoのリセット・電源入れ直し**
   - まず `mpremote connect <デバイス名> reset` でPicoをリセット。
   - それでも改善しない場合はUSBケーブルを抜き差しして電源を入れ直してください。

1. **USB経由で再デプロイ**
   - `deploy.sh` で main.py などを再度Picoに転送。

2. **ファームウェア初期化→再デプロイ**
   - 上記「シリアルポートが認識されない場合の対処法」の flash_nuke.uf2 → ファームウェア書き込み → deploy.sh の手順を実施。

3. **config.pyやversions.jsonの内容を再確認**
   - WiFi設定やバージョン指定、ファイルURL等に誤りがないか確認。

4. **シリアル出力でエラー内容を確認**
   - mpremoteやscreen等でPicoのシリアル出力を確認し、エラー内容を特定。

5. **OTAサーバー側のファイル・バージョンを再確認**
   - サーバー上のファイルが正しいか、バージョン情報が一致しているか確認。

これらの手順で多くのトラブルは解消します。どうしても復旧しない場合は、初期化からやり直してください。

### 簡単なOTA対応アプリケーションの作成

`lib/ota/ota_enabled_app.py`を使用すると、既存のアプリケーションに簡単にOTA機能を追加できます：

#### 【補足】
OTAマネージャ（lib/ota/ota_manager.py）は初期化時にWiFiインターフェースを必ず一度off/onします。
これにより、Pico Wのネットワーク状態が不安定な場合でも、起動時に自動的に再初期化されます。
アプリ側で個別にWiFiリセット処理を記述する必要はありません。


```python
from machine import Pin, Timer
from ota_lib import OTAManager

# OTAマネージャーのインスタンスを作成
ota_manager = OTAManager()

class MyApp:
    """あなたのアプリケーション"""
    def __init__(self):
        self.led = Pin('LED', Pin.OUT)
        # ... アプリケーションの初期化

    def start(self):
        # アプリケーションの開始処理
        pass

    def stop(self):
        # アプリケーションの停止処理
        pass

def main():
    app = MyApp()

    # OTA機能を有効にしてアプリケーションを実行
    ota_manager.run_with_ota(app, "1.0.0")

if __name__ == "__main__":
    main()
```

### OTAライブラリの特徴

- **必須設定**: `config.py`ファイルが必須（設定不備時は日本語エラー表示）
- **確実な動作**: 設定ファイルがない場合は起動時にエラー終了
- **バックグラウンド更新**: アプリケーション動作中に定期的に更新をチェック
- **簡単統合**: 既存のコードに最小限の変更で追加可能
- **エラーハンドリング**: ネットワークエラーやダウンロード失敗を適切に処理

### 使用例

- `main_ota.py`: 1秒間隔点滅 + OTA機能
- `main_v2_ota.py`: 0.5秒間隔点滅 + OTA機能
- `ota_client.py`: 独立したOTAクライアント（config.py必須、日本語エラー対応）

## 📊 バージョン管理

### versions.json形式

```json
{
  "version": "1.2.0",
  "files": [
    {"name": "main.py", "url": "http://192.168.1.100:8080/main.py"}
  ]
}
```

### バージョン更新手順

1. 新しいアプリケーションファイルを作成
2. `versions.json`のバージョン番号を更新
3. URLパスを新しいファイルに更新
4. HTTPサーバーを再起動

## 🛠️ 開発者向け

### 新機能の追加

1. 新しい`.py`ファイルを作成
2. バージョン番号を適切に設定
3. `versions.json`を更新
4. テスト用のHTTPサーバーで確認

### カスタマイズ

- `config.py`: 基本設定（WiFi、サーバーIP等）**必須ファイル**
lib/ota/ota_manager.py, lib/ota/ota_enabled_app.py: OTA機能のカスタマイズ
- `ota_client.py`: 独立したOTAクライアント（config.py必須、日本語エラー対応）
- `http_server.py`: サーバー側の機能拡張

---
2025/10: OTA信頼性向上のため、WiFiインターフェースのソフトリセット仕様を追加しました。
---

## 📝 ライセンス

MIT License

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/新機能`)
3. 変更をコミット (`git commit -m '新機能を追加'`)
4. ブランチにプッシュ (`git push origin feature/新機能`)
5. プルリクエストを作成

---

**注意**: 実際の使用時は、`config.py`とJSONファイル内のIPアドレスを適切な値に変更してください。
