"""
参照動画:
https://www.youtube.com/watch?v=rJ2nPpYsgZo&list=PLGs0VKk2DiYz8js1SJog21cDhkBqyAhC5&index=101&t=115s

Raspberry Pi Pico - PIO を使用したサーボモーター制御プログラム (複数サーボ対応)
---------------------------------------------------------------------------
【概要】
このプログラムは、Raspberry Pi Pico の PIO (Programmable I/O) を利用して、2つのサーボモーターを同時に制御します。
各サーボモーターは、指定された GPIO ピン（GPIO20 および GPIO21）に接続され、Servo クラスにより
各サーボ用の StateMachine を初期化します。set_angle() メソッドで指定した角度（0°～180°）を PWM パルス幅に変換し、
PWM 信号を出力することでサーボモーターの角度を制御します。なお、サーボモーター2はサーボモーター1の動作と補完関係にあり、
角度は反対方向（180° - angle）に設定されます。

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
- PIO を用いたカスタムアセンブリコード (servo_program) により、PWM 信号を生成してサーボモーターを制御します。
- Servo クラスが各サーボモーター用の StateMachine を初期化し、set_angle() メソッドで角度を PWM パルス幅（500µs～2500µs）
  に変換して信号を出力します。
- メインループでは、サーボモーター1は 0° から 180° へ、サーボモーター2は 180° から 0° へと角度を変更しながら動作し、
  各サイクルごとに 1 秒の待機時間を設けることで、安定した動作を実現しています。
"""

import time

class Servo:
    """
    Raspberry Pi Pico の PIO を用いたサーボモーター制御クラス
    """
    from machine import Pin
    import rp2
    _counter = 0  # 各インスタンスに固有の StateMachine 番号を割り当てるためのクラス変数

    @rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, out_shiftdir=rp2.PIO.SHIFT_RIGHT)
    def servo_program():
        # PIO プログラムの開始位置
        wrap_target()
        mov(x, osr)      # OSR から x レジスタへ値を移動
        mov(y, isr)      # ISR から y レジスタへ値を移動
        set(pins, 0)     # 出力ピンを Low に設定
        label('timeLoop')
        jmp(x_not_y, 'nxt')  # x と y を比較、x が y と等しくなければ 'nxt' へジャンプ
        set(pins, 1)     # 条件に応じて出力ピンを High に設定
        label('nxt')
        jmp(y_dec, 'timeLoop')  # y の値をデクリメントしてループ
        wrap()

    def __init__(self, servo_pin):
        """
        指定したピンに対して StateMachine を初期化する。
        
        Args:
            servo_pin (int): サーボモーターに接続される GPIO ピン番号
        """
        self.sm = rp2.StateMachine(
            Servo._counter,
            Servo.servo_program,
            freq=2000000,
            set_base=Servo.Pin(servo_pin)
        )
        self.sm.active(1)
        self.sm.put(20000)
        self.sm.exec("pull()")
        self.sm.exec("mov(isr, osr)")
        Servo._counter += 1

    def set_angle(self, angle):
        """
        指定した角度に基づいて PWM パルス幅を計算し、サーボモーターの角度を設定する。
        
        Args:
            angle (int): 0～180° の角度
        """
        # 0°で500µs、180°で2500µsとなるように変換
        pulse_width = int(500 + angle * 2000 / 180)
        self.sm.put(pulse_width)
        self.sm.exec("pull()")

def main():
    # GPIO20 (サーボモーター1) と GPIO21 (サーボモーター2) に接続
    servo1 = Servo(20)
    servo2 = Servo(21)

    while True:
        # サーボモーター1は 0°→180°、サーボモーター2は 180°→0° へ動作
        for angle in range(0, 181):
            servo1.set_angle(angle)
            servo2.set_angle(180 - angle)
        time.sleep(1)

        # サーボモーター1は 180°→0°、サーボモーター2は 0°→180° へ動作
        for angle in range(180, -1, -1):
            servo1.set_angle(angle)
            servo2.set_angle(180 - angle)
        time.sleep(1)

if __name__ == "__main__":
    main()
