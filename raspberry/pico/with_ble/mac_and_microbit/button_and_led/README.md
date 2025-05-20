# mac_and_microbit/button_and_led

## 概要

このプロジェクトは、Mac から BLE 経由で micro:bit の LED を制御し、micro:bit のボタン状態や UART メッセージを受信する Python スクリプトです。

- BLE で micro:bit に接続
- キーボード入力で micro:bit の LED を ON/OFF
- micro:bit のボタンA/B押下を検知
- UART 経由で micro:bit からのメッセージを受信

## 必要なもの

- Python 3.7 以上
- [pynput](https://pypi.org/project/pynput/)
- [bleak](https://pypi.org/project/bleak/)
- micro:bit（BLEファームウェア書き込み済み）

## インストール

```sh
pip install bleak pynput
```

## micro:bit 側の準備

1. このリポジトリに含まれる `led_and_button.hex` を micro:bit にドラッグ＆ドロップして書き込みます。
2. 書き込み後、micro:bit の電源を入れて BLE で接続待機状態にします。
3. ボタンA/Bの押下やLEDのON/OFF制御ができるようになります。

## 使い方

1. micro:bit の電源を入れ、BLEでペアリング可能な状態にします。
2. Mac で本リポジトリの [`mac_main.py`](mac_main.py) を実行します。

```sh
python3 mac_main.py
```

3. コマンド一覧が表示されます。

```
Commands:
  [1] ON  → LED ON
  [2] OFF → LED OFF
  [q] Quit → 終了
```

- `1` キー: micro:bit の LED を ON
- `2` キー: micro:bit の LED を OFF
- `q` キー: プログラム終了

micro:bit のボタンA/Bを押すと、コンソールに通知が表示されます。

## ファイル構成

- [`mac_main.py`](mac_main.py) : メインスクリプト

## 注意事項

- BLE接続にはMacのBluetoothが有効である必要があります。
- micro:bit 側のファームウェアが対応している必要があります。

## ライセンス

MIT
