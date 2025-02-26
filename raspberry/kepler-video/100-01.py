"""
参照動画:
https://www.youtube.com/watch?v=rJ2nPpYsgZo&list=PLGs0VKk2DiYz8js1SJog21cDhkBqyAhC5&index=101&t=115s

Raspberry Pi Pico - PIO を使用したサーボモーター制御プログラム (複数サーボ対応)
---------------------------------------------------------------------------
【概要】
このプログラムは、Raspberry Pi Pico の PIO (Programmable I/O) を利用して
2つのサーボモーターを制御します。サーボモーターはそれぞれ GPIO20 と GPIO21 に接続されており、
サーボモーター1 (GPIO20) は 0° から 180° へ、サーボモーター2 (GPIO21) は 180° から 0° へ
逆方向に動作します。PIO による PWM 信号生成を用いて、各サーボの角度を精密に制御します。

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
- PIO を用いて PWM 信号を生成し、サーボモーターの角度を制御します。
- サーボモーター1は 0° から 180° へ、サーボモーター2は 180° から 0° へ
  1° ずつ角度を変化させます。
- 各角度変更後、1秒間の待機時間を設け、動作を安定させています。
"""

import time
from machine import Pin
import rp2

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

# PIO の StateMachine 設定
# サーボモーター1 用 (GPIO20)
sm0 = rp2.StateMachine(0, servoSet, freq=2000000, set_base=Pin(20))
sm0.active(1)
sm0.put(20000)
sm0.exec("pull()")
sm0.exec("mov(isr, osr)")

# サーボモーター2 用 (GPIO21)
sm1 = rp2.StateMachine(1, servoSet, freq=2000000, set_base=Pin(21))
sm1.active(1)
sm1.put(20000)
sm1.exec("pull()")
sm1.exec("mov(isr, osr)")

while True:
    # サーボモーター1 は 0°→180° へ、サーボモーター2 は 180°→0° へ動作
    for angle in range(0, 181, 1):
        # 角度を PWM パルス幅に変換（500µs〜2500µs の範囲）
        pw = int(500 + angle * 2000 / 180)
        sm0.put(pw)
        sm0.exec("pull()")
        sm1.put(3000 - pw)  # 補完動作：角度が反対方向になるように設定
        sm1.exec("pull()")
    time.sleep(1)
    
    for angle in range(180, -1, -1):
        pw = int(500 + angle * 2000 / 180)
        sm0.put(pw)
        sm0.exec("pull()")
        sm1.put(3000 - pw)
        sm1.exec("pull()")
