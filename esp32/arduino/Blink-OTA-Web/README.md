
# Blink-OTA-Web

## 目次


- [機能](#機能)
- [必要なもの](#必要なもの)
- [使い方](#使い方)
- [bin ファイルの書き出し方法](#binファイルの書き出し方法)
- [Web 画面で bin ファイルを設定・再設定する手順](#web画面でbinファイルを設定再設定する手順)
- [配線例](#配線例)
- [参考](#参考)

ESP32 DevKitC v4 用 LED 点滅サンプル (Blink) に Web サーバー経由の OTA アップデート機能を追加したスケッチです。

---

## 機能

- GPIO4 ピンに接続した LED を 1 秒ごとに点滅
- Web ブラウザからファームウェア (.bin) をアップロードして OTA 書き換え

---

## 必要なもの

- ESP32 DevKitC v4
- LED、抵抗
- [WiFi (ESP32 標準)](https://github.com/espressif/arduino-esp32)
- [WebServer (ESP32 標準)](https://github.com/espressif/arduino-esp32)
- [Update (ESP32 標準)](https://github.com/espressif/arduino-esp32)

---

## 使い方

1. `Blink-OTA-Web.ino` の `ssid` と `password` をご自身の WiFi 環境に合わせて書き換えます。
2. 必要なライブラリがインストールされていることを確認します。
3. USB 経由で ESP32 にスケッチを書き込みます。
4. ESP32 が WiFi に接続されると、シリアルモニタに IP アドレスが表示されます。
5. Web ブラウザで `http://<ESP32の IP アドレス>/update` にアクセスし、ファームウェア (.bin) をアップロードします。
6. アップデート成功後、自動で再起動します。

---

## binファイルの書き出し方法

**Arduino IDE の場合**

1. 「スケッチ」→「コンパイルしたバイナリを出力」を選択
2. `build/esp32.esp32.esp32doit-devkit-v1/` フォルダ内に `Blink-OTA-Web.ino.bin` などが生成されます

**PlatformIO の場合**

1. `pio run` コマンドでビルド
2. `.pio/build/esp32dev/` などのフォルダに bin ファイルが生成されます

---

## Web画面でbinファイルを設定・再設定する手順


### 詳細な手順

1. ESP32 の IP アドレスをシリアルモニタ等で確認します。
2. Web ブラウザで `http://<ESP32の IP アドレス>/update` にアクセスします。
	- 「OTA Update」リンクからも遷移できます。
	- `http://<ESP32の IP アドレス>/`（トップページ）にアクセスした場合は、「ESP32 Blink-OTA Web」というタイトルと「OTA Update」へのリンクが表示されます。
	- 「OTA Update」リンクをクリックすると、ファームウェアアップデート画面（/update）に移動します。
3. 「ファイルを選択」ボタン（または「参照」ボタン）をクリックし、
	`build/esp32.esp32.esp32doit-devkit-v1/Blink-OTA-Web.ino.bin` を選択します。
4. 「Update」ボタンをクリックするとアップロードが始まります。
	- 進捗バーやメッセージが表示されます。
5. アップロードが完了すると「Success」などのメッセージが表示され、ESP32 が自動的に再起動します。
	- 数秒後に新しいファームウェアが動作します。
6. 別の bin ファイルで再度アップデートしたい場合も、同じ手順で何度でもアップロード可能です。

#### 失敗時の対応
- アップデート中にエラーや失敗メッセージが出た場合は、
  - USB 経由で再度書き込み直すことで復旧できます。
- アップデート中は絶対に電源を切らないでください。

### 注意事項

- アップロードするファイルは必ず `.bin` 拡張子のファームウェア（`Blink-OTA-Web.ino.bin`）を選択してください
- `Blink-OTA-Web.ino.merged.bin` はフル書き込み用です。通常の OTA アップデートでは使用しないでください
- アップデート中は電源を切らないでください
- 何度でも Web 経由で bin ファイルを書き換え可能です
- アップデートに失敗した場合は、USB 経由で書き込み直すことで復旧できます
- アップロードする bin ファイルは、必ず現在のボード設定やピンアサインに合ったものを選んでください

---

## 配線例

- GPIO4 ピンに LED のアノード（長い足）
- LED のカソード（短い足）を抵抗経由で GND

---

## 参考

- [ESP32 Arduino OTA Web Updater 公式ドキュメント](https://github.com/espressif/arduino-esp32/blob/master/libraries/WebServer/examples/OTAWebUpdater/OTAWebUpdater.ino)
- アップデート後は自動的に再起動します。
