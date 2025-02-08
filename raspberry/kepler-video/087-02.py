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
 3. `sm.active(1)` で PIO を開始し、LED を点灯したままにする。
 4. 2秒間 LED を点灯した後、`sm.active(0)` で PIO を停止。
 5. `all_off()` により、プログラム終了時にすべての LED を消灯。

【注意】
  - LED には適切な抵抗 (例: 330Ω) を直列に接続し、過電流を防ぐこと。
  - PIO のプログラムは `set(pins, 0b1001)` を一度実行するのみで、点滅動作は行わない。
  - `freq` は 1_000Hz 以上 125_000_000Hz 以下の範囲で設定すること。
"""

import utime
from machine import Pin
import rp2

@rp2.asm_pio(set_init=(rp2.PIO.OUT_LOW,) * 4, out_init=(rp2.PIO.OUT_LOW,) * 4, out_shiftdir=rp2.PIO.SHIFT_LEFT)
def pio_prog():
    set(pins, 0b1001) # GPIO12 と GPIO15 を HIGH に設定

class LEDController:
    def __init__(self, sm_id, base_pin, freq=1_000_000):  # 適切な範囲のデフォルト値を設定
        if not (1_000 <= freq <= 125_000_000):  # RP2040のPIO範囲に適合
            raise ValueError("freq out of range. Use a value between 1_000 and 125_000_000 Hz")
        self.sm = rp2.StateMachine(sm_id, pio_prog, freq=freq, set_base=Pin(base_pin), out_base=Pin(base_pin))

    def start(self):
        self.sm.active(1)

    def stop(self):
        self.sm.active(0)
        self.all_off()

    def all_off(self):
        for i in range(4):
            Pin(12 + i, Pin.OUT).off()  # GPIO12-15をすべて消灯

# PIO ステートマシンのインスタンス化
led_controller = LEDController(sm_id=0, base_pin=12, freq=1_000_000)  # 適正な周波数を設定

# 5回カウント
for i in range(5):
    utime.sleep(0.5)
    print(i)

# LED 点灯
led_controller.start()

# 2秒間 LED 点灯
utime.sleep(2)

# LED 消灯
led_controller.stop()
