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

def redBlinker(source):
    redLED.toggle()
    Timer(period=100, mode=Timer.ONE_SHOT, callback=turnRedOff)

def turnRedOff(source):
    redLED.off()

def greenBlinker(source):
    greenLED.toggle()

def blueBlinker(source):
    blueLED.toggle()

# タイマーの設定
redTime = Timer(period=1000, mode=Timer.PERIODIC, callback=redBlinker)
greenTime = Timer(period=1000, mode=Timer.PERIODIC, callback=greenBlinker)
blueTime = Timer(period=4000, mode=Timer.PERIODIC, callback=blueBlinker)

try:
    x = 0
    while True:
        print(x)
        utime.sleep(1)
        x += 1
except KeyboardInterrupt:
    # タイマーの停止
    redTime.deinit()
    greenTime.deinit()
    blueTime.deinit()
    
    # LED の消灯
    redLED.off()
    greenLED.off()
    blueLED.off()
