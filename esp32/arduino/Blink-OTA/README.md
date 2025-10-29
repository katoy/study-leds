# Blink-OTA


このスケッチは、ESP32 DevKitC v4 用の LED 点滅サンプル (Blink) に OTA (Over The Air) アップデート機能を追加したものです。
WiFi経由でスケッチを書き換え可能です。

## 機能

- GPIO4 ピンに接続した LED を 1 秒ごとに点滅
- WiFi 経由での OTA アップデート対応

## 使い方

1. `Blink-OTA.ino` の `ssid` と `password` をご自身の WiFi 環境に合わせて書き換えてください。
	- 例:
	  ```cpp
	  const char* ssid = "zzzzzz";
	  const char* password = "zzzzzz";
	  ```
2. 必要なライブラリ（`WiFi.h`, `ArduinoOTA.h`）がインストールされていることを確認してください。
	- Arduino IDE の「ライブラリを管理」から ESP32 ボード用ライブラリを導入してください。
3. 最初はUSB経由でESP32にスケッチを書き込みます。
4. ESP32がWiFiに接続されると、シリアルモニタにIPアドレスが表示されます。
5. 以降は、**コードを変更した後、USB接続なしでOTA経由で書き込みが可能**です。

### OTAでボードへ転送する手順（Arduino IDEの場合）

1. コードを編集し保存します。
2. Arduino IDEの「ツール > ポート」から、ネットワークポート（例: `esp32-blink-ota at 192.168.x.x`）を選択します。
	- ネットワークポートが表示されない場合は、PCとESP32が同じネットワークに接続されているか確認してください。
3. 「マイコンボードに書き込む」ボタンを押すと、OTA経由でESP32に転送されます。
4. 転送中はESP32のシリアルモニタやIDEの出力にOTA進行状況が表示されます。
5. 書き込み完了後、ESP32が自動で再起動し新しいコードが動作します。

**注意:**
- OTA書き込みは、ESP32がWiFiに接続されている必要があります。
- ネットワーク環境によってはファイアウォール等でポートがブロックされている場合、OTAが利用できないことがあります。

## 必要なライブラリ

- [WiFi (ESP32 標準)](https://github.com/espressif/arduino-esp32)
- [ArduinoOTA (ESP32 標準)](https://github.com/espressif/arduino-esp32)

## 配線例

- GPIO4 ピンに LED のアノード（長い足）
- LED のカソード（短い足）を抵抗経由で GND

## 参考

- [ArduinoOTA 公式ドキュメント](https://arduino-esp32.readthedocs.io/en/latest/ota.html)
