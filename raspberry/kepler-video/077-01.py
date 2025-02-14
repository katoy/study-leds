"""
IRリモコン受信プログラム (Raspberry Pi Pico + IR受信モジュール)

このプログラムは NECフォーマットの赤外線リモコンを受信し、
特定のボタンに対応するコマンドをリストに記録し、
記録された数値をサーボモータの角度として設定します。

【配線図】
```
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO18 (IR)   ---+---[IR Receiver]--- GND
        |                |
        |  GPIO19 (Servo) ---+---[Servo Signal]
        |                |
        +----------------+
```

【接続】
  - IR受信モジュール:
    - VCC → Picoの3.3V
    - GND → PicoのGND
    - OUT → PicoのGPIO18
  - サーボモータ:
    - VCC → Picoの5V (または外部電源)
    - GND → PicoのGND
    - Signal → PicoのGPIO19

【動作】
 1. 赤外線リモコンのボタンを押すと、対応するコマンドがリストに記録される。
 2. `POWER` ボタンを押すと記録開始。
 3. 数字ボタンを押すと、サーボの角度情報が記録される。
 4. `ENTER` ボタンを押すと記録を確定し、サーボの角度を変更する。
 5. `Ctrl+C` を押すとプログラムが終了する。

【注意】
  - 赤外線リモコンは NECフォーマットを使用すること。
  - IRモジュールとサーボの電源は適切に供給すること。
  - サーボモータの負荷が大きい場合は外部電源を使用すること。
"""

from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx.print_error import print_error
from servo import servo

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

SERVO_PIN = 19
myServo = servo(SERVO_PIN)

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
            
            numbers = [str(x) for x in new_command if isinstance(x, int)]  # 数値のみを抽出
            print(numbers)
            angle = int("".join(numbers)) if numbers else 0  # 数値があれば結合、なければ0
            print(angle)
            myServo.pos(angle)

            command_ready = False

except KeyboardInterrupt:
    IR.close()
    print("Program terminated")
