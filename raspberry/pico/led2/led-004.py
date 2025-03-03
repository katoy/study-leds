"""
PIO-based LED Blink Example using autopush on Raspberry Pi Pico

概要:
  このスクリプトは、MicroPython と Raspberry Pi Pico の PIO (Programmable I/O) 機能を利用して、
  GPIO15 に接続された LED を 1 秒ごとに点灯・消灯させる例です。
  PIO の `autopush` を活用し、Python 側からのデータ供給を最小限に抑えています。

点滅仕様:
  - GPIO15 (LED) は 1 秒間隔で点滅
  - PIO が `autopush` を利用してタイミング情報を Python 側に送信

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
  - rp2 ライブラリを使用

特徴:
  - PIO による正確なタイミング制御
  - `autopush` を活用し、Python 側の負担を軽減
  - `Ctrl-C` で中断時に LED が確実に消灯する仕組みを実装

作成者:
  [Your Name]

作成日:
  2025-03-03
"""

import rp2
from machine import Pin
import time

# LED 点滅制御用の PIO プログラム
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32, autopush=True, push_thresh=32)
def blink():
    set(pins, 1)       .side(1)  # LED ON
    pull()                      # FIFO から遅延カウントを取得
    mov(x, osr)
    label("delay_on")
    set(y, 31)
    label("inner_on")
    nop()
    jmp(y_dec, "inner_on")
    jmp(x_dec, "delay_on")

    set(pins, 0)       .side(0)  # LED OFF
    pull()
    mov(x, osr)
    label("delay_off")
    set(y, 31)
    label("inner_off")
    nop()
    jmp(y_dec, "inner_off")
    jmp(x_dec, "delay_off")

    mov(isr, x)  # Python 側にカウントを送る
    push()       # FIFO にプッシュ (autopush により自動送信)
    wrap()

# StateMachine 設定
sm = rp2.StateMachine(0, blink, freq=2000000, sideset_base=Pin(15))
sm.active(1)

# 遅延カウント設定 (1 秒)
DELAY_COUNT = 60606

# **FIFO に 1回だけデータを投入**
sm.put(DELAY_COUNT)
sm.put(DELAY_COUNT)

try:
    while True:
        time.sleep(1)  # **ループ内では sleep するだけ**
except KeyboardInterrupt:
    print("Interrupted! Stopping state machine and turning off LED.")
    sm.active(0)
    Pin(15, Pin.OUT).value(0)  # 明示的に LED をオフ
