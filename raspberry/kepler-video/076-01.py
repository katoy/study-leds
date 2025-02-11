"""
IRリモコン受信プログラム (Raspberry Pi Pico + IR受信モジュール)

このプログラムは NECフォーマットの赤外線リモコンを受信し、
特定のボタンに対応するコマンドをリストに記録します。

【配線図】
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO18 (IR)   ---+---[IR Receiver]--- GND
        |                |
        +----------------+

IR受信モジュールの接続:
  - IRモジュールのVCC → Picoの3.3V
  - IRモジュールのGND → PicoのGND
  - IRモジュールのOUT → PicoのGPIO18

"""

from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx.print_error import print_error

# 赤外線リモコンのボタンコードと対応するコマンド
IR_DICT = {
    69: 'POWER', 70: 'MODE', 71: 'OFF',
    68: 'PLAY', 64: 'BACK', 67: 'FORWARD',
    7: 'ENTER', 21: '-', 9: '+',
    22: 0, 25: 'LOOP', 13: 'USD',
    12: 1, 24: 2, 94: 3,
    8: 4, 28: 5, 90: 6,
    66: 7, 82: 8, 74: 9
}

new_command = []
begin_record = False
command_ready = False

IR_PIN = 18  # IR受信機を接続するGPIOピン
myIR = Pin(IR_PIN, Pin.IN)

def callback(ir_bit, addr, ctrl):
    """
    赤外線リモコンの信号を処理するコールバック関数
    """
    global new_command, begin_record, command_ready
    
    if ir_bit == 69:  # POWERボタンで記録開始
        begin_record = True
        new_command = []
        command_ready = False

    if begin_record and ir_bit != -1:
        command = IR_DICT.get(ir_bit)
        if command is not None:
            new_command.append(command)

    if ir_bit == 7:  # ENTERボタンで記録完了
        command_ready = True

IR = NEC_8(myIR, callback)

try:
    while True:
        if command_ready:
            print(new_command)
            command_ready = False

except KeyboardInterrupt:
    IR.close()
    print("Program terminated")
