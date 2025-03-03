"""
LED Blink Example on Raspberry Pi Pico (Using PIO with CPU-side FIFO Re-supply)
==============================================================================
概要:
  このスクリプトは、MicroPython と Raspberry Pi Pico の PIO (Programmable I/O)
  を用いて、GPIO15 に接続された LED を 0.1 秒間オン、0.9 秒間オフの間隔で点滅させる例です。
  2 つの StateMachine (trigger_sm と blink_sm) を使用し、CPU 側の while ループで定期的に
  各 StateMachine の FIFO に遅延値を再供給することで、連続的な点滅動作を実現しています。

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
  - 2 つの PIO StateMachine (trigger_sm と blink_sm) を使用して LED の点滅を実現
  - CPU 側のループで定期的に FIFO を再供給することで連続点滅を実現
  - Ctrl-C で中断時に LED が確実に消灯する仕組みを実装
"""

import rp2
from machine import Pin
import time

# クロック周波数の定義 (2MHz)
CLOCK_FREQ = 2_000_000  # 2MHz

# 定数定義
DELAY_TRIGGER = 2000000  # trigger_sm 用：1秒遅延 (2MHzなら約2000000サイクル)
DELAY_BLINK   = 200000   # blink_sm 用：0.1秒遅延 (2MHzなら約200000サイクル)

# ---------------------------------------------------------
# PIO プログラム: trigger_sm
# ---------------------------------------------------------
# 機能:
#   FIFO から DELAY_TRIGGER の値を受け取り、delay ループで約1秒の遅延を発生させた後、
#   irq(1, 0) により blink_sm をトリガします。
#   CPU 側で定期的に sm.put() により再供給される値を利用します。
@rp2.asm_pio(autopull=True, pull_thresh=32)
def trigger():
    wrap_target()
    pull()                # FIFO から 32bit 値（delay 値）を取得
    mov(x, osr)           # x レジスタにロード
    label("delay")
    jmp(x_dec, "delay")   # x が 0 になるまで 1サイクルずつデクリメント（約1秒遅延）
    irq(1, 0)             # IRQ0 をセットして blink_sm をトリガ
    wrap()

# ---------------------------------------------------------
# PIO プログラム: blink_sm
# ---------------------------------------------------------
# 機能:
#   trigger_sm からの IRQ を待機し、IRQ を受信後に FIFO から DELAY_BLINK の値を取得して、
#   delay ループで約0.1秒間 LED を点灯させた後、LED を消灯します。
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32)
def blink():
    wrap_target()
    wait(1, irq, 0)       # trigger_sm からの IRQ0 を待機
    set(pins, 1) .side(1)  # LED を ON にする
    pull()                # FIFO から 32bit 値（blink delay）を取得
    mov(x, osr)
    label("blink_delay")
    jmp(x_dec, "blink_delay")  # x が 0 になるまでループ（約0.1秒の遅延）
    set(pins, 0) .side(0)  # LED を OFF にする
    wrap()

# ---------------------------------------------------------
# StateMachine の生成と起動
# ---------------------------------------------------------
trigger_sm = rp2.StateMachine(1, trigger, freq=CLOCK_FREQ)
blink_sm   = rp2.StateMachine(0, blink, freq=CLOCK_FREQ, sideset_base=Pin(15))

trigger_sm.active(1)
blink_sm.active(1)

# 初期投入: 各 StateMachine に 1 回だけ遅延値を投入する
trigger_sm.put(DELAY_TRIGGER)
blink_sm.put(DELAY_BLINK)

# ---------------------------------------------------------
# CPU 側のメインループ: 定期的に各 StateMachine の FIFO に再供給する
# ---------------------------------------------------------
try:
    while True:
        time.sleep(1)  # 1秒待機
        trigger_sm.put(DELAY_TRIGGER)
        blink_sm.put(DELAY_BLINK)
except KeyboardInterrupt:
    trigger_sm.active(0)
    blink_sm.active(0)
    Pin(15, Pin.OUT).value(0)
