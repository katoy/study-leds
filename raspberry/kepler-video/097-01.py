"""
Raspberry Pi Pico - サーボモータ制御プログラム

【概要】
- GPIO20 を使用してサーボモータを制御する。
- サーボの角度に応じた PWM 信号を生成する。
- 角度 0° に対応する PWM を初期値として設定。

【配線図】
```
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO20 (Servo) ---+---[Servo Signal]
        |                |
        +----------------+
```

【使用部品】
- Raspberry Pi Pico
- サーボモータ (SG90 など)
- 電源 (3.3V または 5V, 外部電源推奨)

【接続】
- サーボモータのVCC → Picoの5V (または外部電源)
- サーボモータのGND → PicoのGND
- サーボモータのSignal → PicoのGPIO20

【動作】
- 角度 0° の PWM 信号 (500µs) を生成。
- 20ms の周期で PWM を出力し続ける。
- 角度変更時には `pw` を調整し、新しいパルス幅を適用可能。

【注意】
- サーボモータの電源が不足すると動作が不安定になるため、外部電源を使用することを推奨。
- PWM 周期を 20ms (50Hz) に設定し、サーボの動作仕様に適合させる。
"""

import utime
from machine import Pin

servoPin = Pin(20, Pin.OUT)

angle = 0
pw0 = int(angle * 2000 / 180 + 500)
off_us0 = 20000 - pw0

angle = 90
pw90 = int(angle * 2000 / 180 + 500)
off_us90 = 20000 - pw90

while True:
    servoPin.on()
    utime.sleep_us(pw0)
    servoPin.off()
    utime.sleep_us(off_us0)
    utime.sleep(2)
    
    servoPin.on()
    utime.sleep_us(pw90)
    servoPin.off()
    utime.sleep_us(off_us90)
    utime.sleep(2)
