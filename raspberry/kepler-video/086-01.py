"""
Raspberry Pi Pico - ボタン押下による LED トグルスクリプト

このスクリプトは、ボタンの押下を割り込み (IRQ) で検出し、
LED の ON/OFF を切り替えます。

【配線図】

      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO16 (Button) ---+---[Button]--- GND
        |                |
        |  GPIO15 (LED)  ---+---[330Ω]---|>|--- GND
        |                |
        +----------------+
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
buttonPinUp = 16  # ボタンの GPIO ピン
buttonPinDown = 17  # ボタンの GPIO ピン
ledPin1 = 12      # LED の GPIO ピン
ledPin2 = 13      # LED の GPIO ピン
ledPin4 = 14      # LED の GPIO ピン
ledPin8 = 15      # LED の GPIO ピン

# 変数初期化
press = 0

t1Up = utime.ticks_ms()
t1Down = utime.ticks_ms()
buttonState1Old = 0

t2Up = utime.ticks_ms()
t2Down = utime.ticks_ms()
buttonState2Old = 0

def allOffLED():
    led1.off()
    led2.off()
    led4.off()
    led8.off()
    
def setLED(count):
    allOffLED()
    if count & 0x01 == 0x01:
        led1.value(1)
    if count & 0x02 == 0x02:
        led2.value(1)
    if count & 0x04 == 0x04:
        led4.value(1)
    if count % 0x08 == 0x08:
        led8.value(1)

def IntSwitchUp(pin):
    global press, t1Up, t1Down, buttonState1Old
    
    buttonState1 = watchButtonUp.value()
    if buttonState1 == 1:
        t1Down = utime.ticks_ms()
    if buttonState1 == 0:
        t1Up = utime.ticks_ms()
    if buttonState1Old == 0 and buttonState1 == 1 and utime.ticks_diff(t1Down, t1Up) > 25:
        press += 1
        print('TRIGGERED', press)
        setLED(press)
    buttonState1Old = buttonState1

def IntSwitchDown(pin):
    global press, t2Up, t2Down, buttonState2Old
    
    buttonState2 = watchButtonDown.value()
    if buttonState2 == 1:
        t2Down = utime.ticks_ms()
    if buttonState2 == 0:
        t2Up = utime.ticks_ms()
    if buttonState2Old == 0 and buttonState2 == 1 and utime.ticks_diff(t2Down, t2Up) > 25:
        press -= 1
        print('TRIGGERED', press)
        setLED(press)
    buttonState2Old = buttonState2

# ピンの設定
led1 = Pin(ledPin1, Pin.OUT)  # LED 出力
led2 = Pin(ledPin2, Pin.OUT)  # LED 出力
led4 = Pin(ledPin4, Pin.OUT)  # LED 出力
led8 = Pin(ledPin8, Pin.OUT)  # LED 出力

watchButtonUp = Pin(buttonPinUp, Pin.IN, Pin.PULL_DOWN)  # ボタン入力 (プルダウン)
watchButtonDown = Pin(buttonPinDown, Pin.IN, Pin.PULL_DOWN)  # ボタン入力 (プルダウン)

# 割り込み設定
watchButtonUp.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=IntSwitchUp)
watchButtonDown.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=IntSwitchDown)

try:
    while True:
        pass  # メインループは空実行 (割り込みで処理)
        
except KeyboardInterrupt:
    allOffLED()