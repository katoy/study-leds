"""
LED ブリンクプログラム (Raspberry Pi Pico)

このプログラムは、Raspberry Pi Pico の GPIO に接続された LED を
マルチタイマーを使用して異なる周期で点滅させるものです。

【動作概要】
- 10ms ごとにタイマー割り込みを発生
- 1000ms (1秒) ごとに赤 LED (GPIO15) をトグル
- 500ms ごとに緑 LED (GPIO14) をトグル
- 200ms ごとに青 LED (GPIO13) をトグル
- Ctrl+C でプログラムを終了し、LED を消灯

【配線図】
(Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO15 (Red LED)   ---+---[330Ω]---|>|--- GND
        |  GPIO14 (Green LED) ---+---[330Ω]---|>|--- GND
        |  GPIO13 (Blue LED)  ---+---[330Ω]---|>|--- GND
        |                |
        +----------------+

【接続詳細】
- 赤 LED (GPIO15)
- 緑 LED (GPIO14)
- 青 LED (GPIO13)
- すべての LED は 330Ω 抵抗を介して GND に接続

【ライブラリ】
- `machine.Pin` を使用して GPIO を制御
- `machine.Timer` を使用してタイマー割り込みを設定
- `utime` を使用して時間管理

"""

from machine import Pin, Timer
import utime

# GPIO ピンの設定
redPin = 15
greenPin = 14
bluePin = 13

redLED = Pin(redPin, Pin.OUT)
greenLED = Pin(greenPin, Pin.OUT)
blueLED = Pin(bluePin, Pin.OUT)

# タイマー変数
counter = 0

# 10msごとのタイマーで全てのLEDを制御
def multiBlinker(timer):
    global counter
    counter += 10  # 10msごとにカウント

    if counter % 1000 == 0:
        redLED.toggle()
    if counter % 500 == 0:
        greenLED.toggle()
    if counter % 200 == 0:
        blueLED.toggle()

# 10ms ごとにチェックするタイマーを開始
syncTimer = Timer()
syncTimer.init(period=10, mode=Timer.PERIODIC, callback=multiBlinker)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program Terminated")
    syncTimer.deinit()
    redLED.off()
    greenLED.off()
    blueLED.off()
