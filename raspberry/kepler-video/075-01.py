"""
赤外線リモコン受信プログラム (Raspberry Pi Pico + IR 受信モジュール)

このプログラムは、Raspberry Pi Pico に接続された IR 受信モジュールを使用し、
NEC フォーマットの赤外線リモコン信号を受信して、受信コードを出力します。

【配線図】
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO18 (IR Receiver) ---[IR Module]--- GND
        |                |
        +----------------+

【接続詳細】
- IR 受信モジュールの "OUT" ピンを GPIO18 に接続
- IR 受信モジュールの "VCC" ピンを 3.3V に接続
- IR 受信モジュールの "GND" ピンを GND に接続

【操作】
- 赤外線リモコンのボタンを押すと、対応する IR コードがシリアル出力されます。
- Ctrl+C でプログラムを終了可能。

【ライブラリ】
- `ir_rx.nec.NEC_8` を使用して NEC 形式の IR 信号を解析
"""

from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx.print_error import print_error

# IR 受信モジュールの接続ピン (GPIO18)
IR_PIN = 18
myIR = Pin(IR_PIN, Pin.IN)

# コールバック関数: 受信した IR コードを表示
def callback(IRbit, addr, ctrl):
    print(IRbit)

# IR 受信オブジェクトの作成
IR = NEC_8(myIR, callback)

try:
    while True:
        pass
except KeyboardInterrupt:
    IR.close()
    print("Program terminated")
