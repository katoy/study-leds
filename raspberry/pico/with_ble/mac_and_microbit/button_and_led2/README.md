# button_and_led2

macOS から micro:bit へ BLE (Bluetooth Low Energy) 経由でコマンドを送信し、micro:bit 側のボタン操作やLED制御を行うサンプルプロジェクトです。

## 概要
- `mac_main_bleak.py`: Python の [bleak](https://github.com/hbldh/bleak) ライブラリを用いて、macOS から micro:bit へ BLE UART サービス経由でコマンド送信・受信を行います。
- `mac_main.py`: USB 経由で micro:bit と通信するサンプル（`kaspersmicrobit` ライブラリ使用）。
- `microbit-v2-sample.hex`: micro:bit 側で動作させるファームウェア（バイナリ）。

## 必要環境
- macOS
- Python 3.7 以上
- [bleak](https://pypi.org/project/bleak/)（BLE 通信用）
- [pynput](https://pypi.org/project/pynput/)（キーボード入力用）
- [kaspersmicrobit](https://pypi.org/project/kaspersmicrobit/)（USB 通信用、`mac_main.py` 用）

## セットアップ
```sh
python3 -m pip install bleak pynput kaspersmicrobit
```

## 使い方
### BLE で micro:bit と通信（推奨）
1. micro:bit に `microbit-v2-sample.hex` を書き込む。
2. macOS で以下を実行：
   ```sh
   python3 mac_main_bleak.py
   ```
3. コマンド：
   - `1` : micro:bit に “on” を送信
   - `2` : micro:bit に “off” を送信
   - `q` または `ESC` : 終了

### USB で micro:bit と通信
1. micro:bit に `microbit-v2-sample.hex` を書き込む。
2. micro:bit を USB で接続。
3. macOS で以下を実行：
   ```sh
   python3 mac_main.py
   ```
4. コマンド：
   - `1` : “on” を送信
   - `2` : “off” を送信
   - `q` : 終了

## ファイル説明
- `mac_main_bleak.py` : BLE (Bluetooth Low Energy) で micro:bit と通信するメインスクリプト
- `mac_main.py` : USB 経由で micro:bit と通信するメインスクリプト
- `microbit-v2-sample.hex` : micro:bit 用ファームウェア
- `microbit.png` : micro:bit の画像（参考用）

## ライセンス
MIT License
