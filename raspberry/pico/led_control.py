"""
Raspberry Pi Pico / Pico W 用 内蔵 LED 制御モジュール

このモジュールは、Raspberry Pi Pico と Pico W の内蔵 LED を統一的に制御するためのクラスを提供します。
デバイスに応じた違いを自動的に処理し、以下のメソッドを使用して簡単に LED を制御できます。

機能:
- Raspberry Pi Pico / Pico W を自動判別
- LED の点灯、消灯、トグル（状態切り替え）をサポート
- Ctrl-C で中断された場合でも安全にリソースを解放（後処理）

使用方法:
1. モジュールをインポート
   from led_control import Pico_LED

2. インスタンスを作成
   led = Pico_LED()

3. LED を制御
   led.on()   # LED を点灯
   led.off()  # LED を消灯
   led.toggle()  # LED の状態を切り替え

4. 後処理
   プログラム終了時、または Ctrl-C で中断された際に cleanup() メソッドを呼び出してリソースを解放します。

例:
try:
    while True:
        led.toggle()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("中断されました。")
finally:
    led.cleanup()

対応デバイス:
- Raspberry Pi Pico
- Raspberry Pi Pico W
"""

import os
from machine import Pin, PWM


class Pico_LED:
    """
    Raspberry Pi Pico / Pico W の内蔵 LED を制御するクラス
    """

    def __init__(self):
        """
        Pico_LED インスタンスを初期化します。
        デバイスを判別して適切に設定します。
        """
        if self.is_pico_w():
            # Pico W: PWM を使用して内蔵 LED を制御
            self.led = Pin("LED", Pin.OUT)
        else:
            # Pico: GPIO 25 を使用して内蔵 LED を制御
            self.led = Pin(25, Pin.OUT)

        self.is_pwm = False

    @staticmethod
    def is_pico_w():
        """
        現在のデバイスが Raspberry Pi Pico W かを判定します。
        Returns:
            bool: True - Pico W、False - その他
        """
        return "RP2040" in os.uname().machine and "Pico W" in os.uname().machine

    def on(self):
        """
        LED を点灯します。
        """
        if self.is_pwm:
            self.led.duty_u16(65535)  # 最大の明るさ
        else:
            self.led.on()

    def off(self):
        """
        LED を消灯します。
        """
        if self.is_pwm:
            self.led.duty_u16(0)  # 消灯
        else:
            self.led.off()

    def toggle(self):
        """
        LED の状態を切り替えます（点灯 → 消灯、またはその逆）。
        """
        if self.is_pwm:
            # PWM の状態を反転
            if self.led.duty_u16() > 0:
                self.led.duty_u16(0)
            else:
                self.led.duty_u16(65535)
        else:
            # GPIO の状態を反転
            if self.led.value() == 1:
                self.led.off()
            else:
                self.led.on()

    def cleanup(self):
        """
        LED を消灯し、リソースを解放します。
        """
        if self.is_pwm:
            self.led.duty_u16(0)  # 消灯
            self.led.deinit()     # PWM を無効化
        else:
            self.led.off()        # GPIO LED を消灯
        print("LED の後処理が完了しました。")

