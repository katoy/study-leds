"""
Raspberry Pi Pico を用いたボタン入力と LED 点灯プログラム

【概要】
GPIO16 に接続されたボタンを押すと、GPIO15 に接続された LED の状態が切り替わります。

【配線図】
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO16 (Button) ---+---[Button]--- GND
        |                |
        |  GPIO15 (LED)  ---+---[330Ω]---|>|--- GND
        |                |
        +----------------+

【注意】
LED には適切な抵抗（例：330Ω）を接続してください。
抵抗なしでは過電流により LED や Pico が破損する恐れがあります。

"""

from machine import Pin
import utime

# GPIOピンの設定
BUTTON_PIN = 16  # ボタン接続ピン
LED_PIN = 15     # LED接続ピン

# ボタンが押された回数を記録する変数
press_count = 0

# 割り込みハンドラ関数
def button_interrupt(pin):
    global press_count
    press_count += 1
    print(f'TRIGGERED {press_count}')
    led.toggle()

# LED とボタンのピンを設定
led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)

# 割り込みを設定（ボタンが押されたときに実行）
button.irq(trigger=Pin.IRQ_RISING, handler=button_interrupt)

try:
    while True:
        pass  # メインループは空で待機
except KeyboardInterrupt:
    led.off()  # 終了時に LED を消灯
