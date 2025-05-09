"""
toggle_led.py

概要:
    GPIO16 に接続したプルアップ付きボタンで内蔵LED（GP25）をトグル制御するスクリプト。
    起動直後は LED が ON になり、Ctrl-C で終了すると LED が OFF になります。

配線方法:
    タクトスイッチ:
        - 一端を GPIO16 (GP16)
        - 他端を GND
        - 内部プルアップを利用（外部抵抗不要）

    内蔵LED:
        - GP25 に接続済み（基板内蔵）

簡易配線図:
        +3.3V
          │
      (内部プルアップ)
          │
       GP16 o───[ SW ]───o GND
          
       内蔵LED: GP25

使用方法:
    1. このファイルを Pico にコピーし、REPL で実行:
       >>> import toggle_led
    2. 起動時に LED が点灯し、ボタンを押すたびにトグル。
    3. Ctrl-C で停止すると LED が消灯します。
"""

from machine import Pin
import time

# GPIO16 にプルアップ付きボタン、内蔵LED は GP25（“LED”）
BUTTON_PIN = 16
LED_PIN    = "LED"

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
led    = Pin(LED_PIN,    Pin.OUT)

# 起動時に LED を ON
led.value(1)

# 前回のボタン状態を保持（プルアップなので押していないときは 1）
prev_state = button.value()

try:
    while True:
        curr_state = button.value()
        # 押し下げの立ち下がり（1→0）を検出したらトグル
        if prev_state == 1 and curr_state == 0:
            # 現在の値を反転させてセット
            led.value(not led.value())
        prev_state = curr_state
        # チャタリング対策に 50ms スリープ
        time.sleep_ms(50)
except KeyboardInterrupt:
    # Ctrl-C で終了するときは LED を OFF に
    led.value(0)
    print("Exiting: LED off")
