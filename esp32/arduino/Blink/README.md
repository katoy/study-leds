# Blink


このプロジェクトは、ESP32-WROOM-32 DevKitC v4 ボードを使った「LED 点滅 (Blink)」サンプルです。


## 概要


ESP32 の GPIO4 ピンに接続した LED を 1 秒ごとに点滅させます。


## ファイル構成

- `Blink.ino` : メインの Arduino スケッチファイル



## Arduino IDEでの準備

### ESP32 ボードの追加手順

1. Arduino IDE を開き、メニューから「Arduino」→「環境設定」を選択します。
2. 「追加のボードマネージャの URL」に以下を追加します：
  - `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
3. 「ツール」→「ボード」→「ボードマネージャ」を開き、「esp32」で検索し「esp32 by Espressif Systems」をインストールします。
4. 「ツール」→「ボード」から「ESP32 Dev Module」または「ESP32 DevKitC」を選択してください。
  - 「ESP32-WROOM-32 DevKitC v4」では「ESP32 DevKitC」または「ESP32 Dev Module」が推奨です。


## 使い方

1. Arduino IDE で `Blink.ino` を開きます。
2. ESP32 ボードを PC に接続し、ボードタイプ (例: ESP32 DevKitC) とポートを選択します。
3. スケッチを書き込みます。
4. GPIO4 ピンに接続した LED が 1 秒ごとに点滅します。


## ブレッドボードでの配線例

ESP32 の GPIO4 ピンを使って LED を点灯・消灯します。以下のように配線してください。

- **GPIO4** → **抵抗 (330Ω 程度)** → **LED のアノード (長い脚)**
- **LED のカソード (短い脚)** → **GND**


```text
┌---------------- ESP32 DevKitC v4 --------------┐
|                                                |
|  o GPIO4                               GND o   |
└----┬-----------------------------------┬-------┘
     │                                   │
   [330Ω]                                │
     │                                   │
   |>| LED                               │
     │                                   │
-----┴-----------------------------------┴-------
ブレッドボード GND ライン
```


**注意:**
- LED の極性 (向き) に注意してください。
  - LED には「アノード (＋、長い脚)」と「カソード (−、短い脚)」があります。
  - アノード (長い脚) を抵抗側、カソード (短い脚) を GND 側に接続してください。
  - 回路図記号「|>|」の上がアノード (＋)、下がカソード (−) です。
- 抵抗値は 330Ω〜1kΩ 程度が目安です。



## 参考リンク

- [Arduino公式 Blink解説](https://docs.arduino.cc/built-in-examples/basics/Blink/)
- [ESP32 Arduino セットアップ手順（公式）](https://docs.espressif.com/projects/arduino-esp32/ja/latest/installing.html)

---



このプロジェクトは学習用です。