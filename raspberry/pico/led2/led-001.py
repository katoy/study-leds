"""
LED Blink Example on Raspberry Pi Pico

概要:
  このスクリプトは、MicroPython を用いて Raspberry Pi Pico 上で GPIO15 に接続された LED を 1 秒ごとに点灯・消灯させる例です。

配線方法:
  図示の例
  【配線図】
  (Raspberry Pi Pico)
          +----------------+
          |                |
          |  GPIO15 (LED)  ---+---[330Ω]---|>|--- GND
          |                |
          +----------------+

動作環境:
  - Raspberry Pi Pico
  - MicroPython 実行環境

作成者:
  [Your Name]

作成日:
  2025-03-02
"""

from machine import Pin
import time

led = Pin(15, Pin.OUT)  # GPIO15 を出力として設定

while True:
    led.value(1)  # LED をオン
    time.sleep(1) # 1秒待つ
    led.value(0)  # LED をオフ
    time.sleep(1) # 1秒待つ
