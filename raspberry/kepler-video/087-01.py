"""
Raspberry Pi Pico - PIO を用いた LED 制御

このスクリプトは、Raspberry Pi Pico の PIO (Programmable I/O) を使用して、
複数の LED を制御するプログラムです。

【配線図】
```
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO12 (LED1)  ---+---[330Ω]---|>|--- GND
        |  GPIO13 (LED2)  ---+---[330Ω]---|>|--- GND
        |  GPIO14 (LED3)  ---+---[330Ω]---|>|--- GND
        |  GPIO15 (LED4)  ---+---[330Ω]---|>|--- GND
        |                |
        +----------------+
```

【使用するピン】
  - GPIO12 (LED1): 出力ピン
  - GPIO13 (LED2): 出力ピン
  - GPIO14 (LED3): 出力ピン
  - GPIO15 (LED4): 出力ピン

【動作】
 1. PIO (Programmable I/O) を利用して LED のパターンを設定。
 2. `set(pins, 0b1001)` により GPIO12, GPIO15 を HIGH に設定し LED を点灯。
 3. `sm0.active(1)` で PIO を開始。
 4. 2秒間 LED を点灯した後、`sm0.active(0)` で PIO を停止。

【注意】
  - LED には適切な抵抗 (例: 330Ω) を直列に接続し、過電流を防ぐこと。
  - PIO のプログラムは `wrap_target()` と `wrap()` を用いることで継続的に動作させることが可能。
  - `freq=1000` などの設定を適用すると動作速度を調整できる。
"""

import utime
from machine import Pin
import rp2

@rp2.asm_pio(set_init=(rp2.PIO.OUT_LOW,) * 4)
def pioProg():
    set(pins, 0b1001)  # GPIO12 と GPIO15 を HIGH に設定

# PIO ステートマシンの設定
sm0 = rp2.StateMachine(0, pioProg, set_base=Pin(12))

# 5回カウント
for i in range(5):
    utime.sleep(0.5)
    print(i)

# PIO の開始
sm0.active(1)

# 2秒間 LED 点灯
utime.sleep(2)

# PIO の停止
sm0.active(0)
