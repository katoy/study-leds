"""
PIO-based Dual LED Blink Example on Raspberry Pi Pico

概要:
  このスクリプトは、MicroPython と Raspberry Pi Pico の PIO (Programmable I/O) 機能を利用して、
  GPIO15 と GPIO14 に接続された 2 つの LED をそれぞれ異なる周期で点滅させる例です。
  PIO アセンブリプログラムを用いて、LED の点灯・消灯を制御し、FIFO へのデータ投入は
  初回のみ 1 回行うことで継続的な点滅を実現しています。

点滅仕様:
  - GPIO15 (LED1) は 1 秒間隔で点滅
  - GPIO14 (LED2) は 0.5 秒間隔で点滅

配線方法:
  【配線図】
  (Raspberry Pi Pico)
          +----------------+
          |                |
          |  GPIO15 (LED1)  ---+---[330Ω]---|>|--- GND
          |                |
          |  GPIO14 (LED2)  ---+---[330Ω]---|>|--- GND
          |                |
          +----------------+

動作環境:
  - Raspberry Pi Pico
  - MicroPython 実行環境
  - rp2 ライブラリを使用

特徴:
  - PIO による正確なタイミング制御
  - FIFO に 1 回だけデータを送ることで継続的な点滅を実現
  - `Ctrl-C` で中断時に LED が確実に消灯する仕組みを実装

作成者:
  [Your Name]

作成日:
  2025-03-03
"""


import rp2
from machine import Pin
import time

# LED 制御用の PIO プログラム (FIFO からのデータを繰り返し使用)
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_HIGH, autopull=True, pull_thresh=32)
def led_control():
    set(pins, 1)     .side(1)  # **プログラム開始時に LED を ON にする**
    label("start")
    wait(1, irq, 0)  # IRQ0 の信号を待つ (GPIO15 用)
    irq(clear, 0)    # IRQ0 をクリア
    set(pins, 1)     .side(1)  # LED をオン
    wait(1, irq, 0)  # 次の IRQ0 の信号を待つ
    irq(clear, 0)    # IRQ0 をクリア
    set(pins, 0)     .side(0)  # LED をオフ
    jmp("start")     # ループ

@rp2.asm_pio(sideset_init=rp2.PIO.OUT_HIGH, autopull=True, pull_thresh=32)
def led_control_14():
    set(pins, 1)     .side(1)  # **プログラム開始時に LED を ON にする**
    label("start")
    wait(1, irq, 1)  # IRQ1 の信号を待つ (GPIO14 用)
    irq(clear, 1)    # IRQ1 をクリア
    set(pins, 1)     .side(1)  # LED をオン
    wait(1, irq, 1)  # 次の IRQ1 の信号を待つ
    irq(clear, 1)    # IRQ1 をクリア
    set(pins, 0)     .side(0)  # LED をオフ
    jmp("start")     # ループ

# タイマー制御用の PIO プログラム
@rp2.asm_pio(autopull=True, pull_thresh=32)
def timer_control():
    label("start")
    pull()           # FIFO から遅延カウントを受信（自動補充）
    mov(x, osr)      # X レジスタに保存
    label("delay")
    set(y, 31)       # 内側ループ用のカウント
    label("inner_loop")
    nop()
    jmp(y_dec, "inner_loop")
    jmp(x_dec, "delay")  # X が 0 になるまでループ
    irq(0)          # GPIO15 用 IRQ
    jmp("start")    # ループ

@rp2.asm_pio(autopull=True, pull_thresh=32)
def timer_control_14():
    label("start")
    pull()           # FIFO から遅延カウントを受信（自動補充）
    mov(x, osr)      # X レジスタに保存
    label("delay")
    set(y, 31)       # 内側ループ用のカウント
    label("inner_loop")
    nop()
    jmp(y_dec, "inner_loop")
    jmp(x_dec, "delay")  # X が 0 になるまでループ
    irq(1)          # GPIO14 用 IRQ
    jmp("start")    # ループ

# **Python 側で GPIO15 と GPIO14 を ON に設定**
pin15 = Pin(15, Pin.OUT)
pin14 = Pin(14, Pin.OUT)
pin15.value(1)
pin14.value(1)

time.sleep(0.1)  # **PIO 開始前に LED ON 状態を維持するための短い遅延**

# LED 制御用 StateMachine (GPIO15)
sm_led_15 = rp2.StateMachine(0, led_control, freq=2000000, sideset_base=pin15)
sm_led_15.active(1)

# LED 制御用 StateMachine (GPIO14)
sm_led_14 = rp2.StateMachine(2, led_control_14, freq=2000000, sideset_base=pin14)
sm_led_14.active(1)

# タイマー制御用 StateMachine (GPIO15用)
sm_timer_15 = rp2.StateMachine(1, timer_control, freq=2000000)
sm_timer_15.active(1)

# タイマー制御用 StateMachine (GPIO14用)
sm_timer_14 = rp2.StateMachine(3, timer_control_14, freq=2000000)
sm_timer_14.active(1)

# 遅延カウント設定 (1 秒と 0.5 秒)
DELAY_COUNT_1S = 60606
DELAY_COUNT_05S = DELAY_COUNT_1S // 2  # 0.5 秒

# **FIFO に 1回だけデータを投入**
sm_timer_15.put(DELAY_COUNT_1S)
sm_timer_14.put(DELAY_COUNT_05S)

try:
    while True:
        time.sleep(1)  # ループ内では sleep するだけ
except KeyboardInterrupt:
    print("\nInterrupted! Stopping state machines and turning off LEDs.")

    # **GPIO を IN にして PIO の影響を完全になくす**
    pin15.init(Pin.IN)
    pin14.init(Pin.IN)

    # **StateMachine を無効化**
    sm_timer_15.active(0)
    sm_timer_14.active(0)
    sm_led_15.active(0)
    sm_led_14.active(0)

    # **GPIO を再び OUT にして LED を OFF にする**
    pin15.init(Pin.OUT)
    pin14.init(Pin.OUT)
    pin15.value(0)
    pin14.value(0)

    print("LEDs turned off.")
