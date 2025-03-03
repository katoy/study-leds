"""
LED Blink Example on Raspberry Pi Pico (Without PIO)

概要:
  このスクリプトは、MicroPython を用いて Raspberry Pi Pico 上で GPIO15 に接続された LED を
  0.1 秒間オン、0.9 秒間オフの間隔で点滅させるシンプルな例です。

配線方法:
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

特徴:
  - PIO を使用せず、シンプルな `while True` ループで LED を制御
  - `Ctrl-C` で中断時に LED が確実に消灯する仕組みを実装

作成者:
  [Your Name]

作成日:
  2025-03-03
"""

from machine import Pin
import time

# GPIO15 を出力として設定
led = Pin(15, Pin.OUT)

try:
    while True:
        led.value(1)  # LED を ON (0.1秒)
        time.sleep(0.1)
        led.value(0)  # LED を OFF (0.9秒)
        time.sleep(0.9)
except KeyboardInterrupt:
    print("Interrupted! Turning off LED.")
    led.value(0)  # 明示的に LED をオフ
