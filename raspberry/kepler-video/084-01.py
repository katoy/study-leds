"""
Raspberry Pi Pico - ボタン押下による LED トグルスクリプト

このスクリプトは、ボタンの押下を割り込み (IRQ) で検出し、
LED の ON/OFF を切り替えます。

【配線図】
```
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO16 (Button) ---+---[Button]--- GND
        |                |
        |  GPIO15 (LED)  ---+---[330Ω]---|>|--- GND
        |                |
        +----------------+
```

【使用するピン】
  - buttonPin (16): プルダウン抵抗を有効化した入力ピン
  - redPin (15): 出力ピン (LED 制御)

【動作】
 1. ボタンが押されると `IntSwitch` が呼び出され、LED をトグルする。
 2. チャタリング防止のために 25ms のディレイをチェック。
 3. 割り込み (IRQ) を利用してボタンの状態を監視。

【注意】
  - LED には適切な抵抗 (例: 330Ω) を直列に接続して、過電流を防ぐこと。
  - `KeyboardInterrupt` によりプログラムを安全に終了可能。
  - タイポ修正: `KEyboardInterrupt` → `KeyboardInterrupt`
"""

from machine import Pin
import utime

# ピン設定
buttonPin = 16  # ボタンの GPIO ピン
redPin = 15     # LED の GPIO ピン

# 変数初期化
press = 0
tUp = utime.ticks_ms()
tDown = utime.ticks_ms()
buttonStateOld = 0

def IntSwitch(pin):
    global press, tUp, tDown, buttonStateOld
    
    buttonState = watchButton.value()
    if buttonState == 1:
        tDown = utime.ticks_ms()
    if buttonState == 0:
        tUp = utime.ticks_ms()
    if buttonStateOld == 0 and buttonState == 1 and (tDown - tUp) > 25:
        press += 1
        print('TRIGGERED', press)
        redLED.toggle()
    buttonStateOld = buttonState

# ピンの設定
redLED = Pin(redPin, Pin.OUT)  # LED 出力
watchButton = Pin(buttonPin, Pin.IN, Pin.PULL_DOWN)  # ボタン入力 (プルダウン)

# 割り込み設定
watchButton.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=IntSwitch)

try:
    while True:
        pass  # メインループは空実行 (割り込みで処理)
        # redLED.toggle()
        # v = watchButton.value()
        # print(v)
        # utime.sleep(1)
        
except KeyboardInterrupt:
    redLED.off()
