"""
Raspberry Pi Pico - ボタンによる LED の制御

このスクリプトは、Raspberry Pi Pico に接続したボタンの押下を割り込み (IRQ) で検出し、
LED の点灯パターンを変更します。

【配線図】
```
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO16 (Button Up) ---+---[Button]--- GND
        |                |
        |  GPIO17 (Button Down) ---+---[Button]--- GND
        |                |
        |  GPIO12 (LED1)  ---+---[330Ω]---|>|--- GND
        |  GPIO13 (LED2)  ---+---[330Ω]---|>|--- GND
        |  GPIO14 (LED4)  ---+---[330Ω]---|>|--- GND
        |  GPIO15 (LED8)  ---+---[330Ω]---|>|--- GND
        |                |
        +----------------+
```

【使用するピン】
  - button_pins: [16, 17] (プルダウン抵抗を有効化した入力ピン)
  - led_pins: [12, 13, 14, 15] (LED 出力ピン)

【動作】
 1. GPIO16 のボタンを押すと LED パターンが増加。
 2. GPIO17 のボタンを押すと LED パターンが減少。
 3. 割り込み (IRQ) によるボタンの状態監視。
 4. チャタリング防止のため 25ms のディレイチェックを実施。

【注意】
  - LED には適切な抵抗 (例: 330Ω) を直列に接続して、過電流を防ぐこと。
  - `KeyboardInterrupt` によりプログラムを安全に終了可能。
"""

from machine import Pin
import utime

# ピン設定
button_pins = [16, 17]  # ボタンの GPIO ピン
led_pins = [12, 13, 14, 15]  # LED の GPIO ピン

# LED ピンの初期化
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# ボタンピンの初期化
buttons = [Pin(pin, Pin.IN, Pin.PULL_DOWN) for pin in button_pins]

# 変数初期化
press = 0
times = {pin: utime.ticks_ms() for pin in button_pins}
button_states = {pin: 0 for pin in button_pins}

def all_off_led():
    for led in leds:
        led.off()

def set_led(count):
    all_off_led()
    for i, led in enumerate(leds):
        if count & (1 << i):
            led.on()

def button_handler(pin):
    global press
    
    # 渡された pin オブジェクトの GPIO 番号を取得
    try:
        pin_number = next(p for p in button_pins if buttons[button_pins.index(p)] == pin)
    except StopIteration:
        return  # 無効なピンの場合は何もしない
    
    current_state = pin.value()
    if current_state == 1:
        times[pin_number] = utime.ticks_ms()
    if current_state == 0 and button_states[pin_number] == 1 and utime.ticks_diff(utime.ticks_ms(), times[pin_number]) > 25:
        press += 1 if pin_number == button_pins[0] else -1
        print(f'TRIGGERED {press}')
        set_led(press)
    button_states[pin_number] = current_state

# 割り込み設定
for button in buttons:
    button.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=button_handler)

try:
    while True:
        pass  # メインループは空実行 (割り込みで処理)
except KeyboardInterrupt:
    all_off_led()
