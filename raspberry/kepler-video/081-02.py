"""
Raspberry Pi Pico を使用した LED ブリンカー

【概要】
- GPIO ピンを使用して、赤・緑・青の LED を点滅させる。
- それぞれ異なる周期で点滅する。
- LED には適切な抵抗を接続する必要がある。

【配線図】
```
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO15 (Red)  ---+---[330Ω]---|>|--- GND
        |  GPIO14 (Green)---+---[330Ω]---|>|--- GND
        |  GPIO13 (Blue) ---+---[330Ω]---|>|--- GND
        |                |
        +----------------+
```

【使用部品】
- Raspberry Pi Pico
- 赤色 LED (Red) 1個
- 緑色 LED (Green) 1個
- 青色 LED (Blue) 1個
- 330Ω 抵抗 3個

【点滅パターン】
- 赤 LED: 0.1秒 ON, 0.9秒 OFF
- 緑 LED: 1秒ごとにトグル
- 青 LED: 4秒ごとに点滅

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

def led_blinker(timer):
    global tick
    tick += 1
    if tick % 10 == 1:  # 100ms (0.1秒) 赤 LED ON
        redLED.on()
    elif tick % 10 == 2:  # 100ms 後に赤 LED OFF
        redLED.off()
    if tick % 10 == 0:  # 1000ms (1秒) ごとに緑 LED
        greenLED.toggle()
    if tick % 40 == 0:  # 4000ms (4秒) ごとに青 LED
        blueLED.toggle()

# タイマーの設定 (100ms間隔)
tick = 0
timer = Timer(period=100, mode=Timer.PERIODIC, callback=led_blinker)

try:
    x = 0
    while True:
        print(x)
        utime.sleep(1)
        x += 1
except KeyboardInterrupt:
    # タイマーの停止
    timer.deinit()
    
    # LED の消灯
    redLED.off()
    greenLED.off()
    blueLED.off()
