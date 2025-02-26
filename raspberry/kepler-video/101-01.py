"""
参照動画:
https://www.youtube.com/watch?v=rJ2nPpYsgZo&list=PLGs0VKk2DiYz8js1SJog21cDhkBqyAhC5&index=101&t=115s

Raspberry Pi Pico - PIO を使用したサーボモーター制御プログラム (複数サーボ対応)
---------------------------------------------------------------------------
【概要】
このプログラムは、Raspberry Pi Pico の PIO (Programmable I/O) を利用して、2つのサーボモーターを同時に制御します。
各サーボモーターは、指定された GPIO ピン（GPIO20 および GPIO21）に接続され、ServoState クラスにより
各サーボ用の StateMachine を初期化します。setAngle() メソッドで指定した角度（0°～180°）を PWM パルス幅に変換し、
PWM 信号を出力することでサーボモーターの角度を制御します。なお、サーボモーター2はサーボモーター1の動作と補完関係にあり、
角度を 180° から逆に設定しています。

【使用ライブラリ】
- machine: GPIO 制御のため
- rp2: PIO 制御のため
- time: 待機時間管理のため

【配線図】
  (Raspberry Pi Pico)
      +-----------------------------------+
      |                                   |
      |  GPIO20  ---[Signal]---> サーボモーター1
      |  GPIO21  ---[Signal]---> サーボモーター2
      |                                   |
      |  GND     ---[共通]---> 全デバイスの GND
      |  5V      ---[電源]---> サーボモーターの Vcc
      +-----------------------------------+

【動作説明】
- PIO を用いたカスタムアセンブリコード (servoSet) により、PWM 信号を生成しサーボモーターを制御します。
- ServoState クラスが各サーボモーター用の StateMachine を初期化し、setAngle() メソッドで角度を PWM パルス幅（500µs～2500µs）
  に変換して信号を出力します。
- メインループでは、サーボモーター1は 0° から 180° へ、サーボモーター2は 180° から 0° へと角度を変更しながら動作し、
  各サイクルごとに 1 秒の待機時間を設けることで、安定した動作を実現しています。
"""

import time
from machine import Pin
import rp2

class ServoState:
    counter = 0
    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
    def servoSet():
        wrap_target()
        mov(x, osr)
        mov(y, isr)
        set(pins, 0)
        label('timeLoop')
        jmp(x_not_y, 'nxt')
        set(pins, 1)
        label('nxt')
        jmp(y_dec, 'timeLoop')    
        wrap()

    def __init__(self, servoPin):
        # PIO の StateMachine 設定
        # サーボモーター1 用 (GPIO20)
        self.sm = rp2.StateMachine(ServoState.counter, ServoState.servoSet, freq=2000000, set_base=Pin(servoPin))
        self.sm.active(1)
        self.sm.put(20000)
        self.sm.exec("pull()")
        self.sm.exec("mov(isr, osr)")
        ServoState.counter += 1

    def setAngle(self, angle):
        pw = int(500 + angle * 2000 / 180)
        self.sm.put(pw)
        self.sm.exec("pull()")

# サーボモーター2 用 (GPIO21)
sm0 = ServoState(20)
sm1 = ServoState(21)

while True:
    # サーボモーター1 は 0°→180° へ、サーボモーター2 は 180°→0° へ動作
    for angle in range(0, 181, 1):
        sm0.setAngle(angle)
        sm1.setAngle(180 - angle)
    time.sleep(1)
    
    for angle in range(180, -1, -1):
        sm0.setAngle(angle)
        sm1.setAngle(180 - angle)

