"""
Raspberry Pi Pico を使用した WS2812 LED 制御用 PIO プログラム
---------------------------------------------------------------------
このプログラムは、Raspberry Pi Pico (RP2040 マイコン) の PIO (Programmable I/O)
を利用して、WS2812 (NeoPixel) LED ストリップに適切なタイミングでデータ信号を
送信するためのアセンブリコードです。さらに、Pico の 5V 出力ピンを利用して LED ストリップに
電源を供給します。

【配線図】

      +-----------------------------+
      |    Raspberry Pi Pico        |
      |                             |
      |    GPIO 0  --------------+  |  ← データ出力 (WS2812 の DIN ピン)
      |                             |
      |    5V      --------------+  |  ← 電源出力 (WS2812 の VDD ピン)
      |                             |
      |    GND     --------------+  |  ← 共通グランド (WS2812 の GND)
      |                             |
      +-----------------------------+

※ Raspberry Pi Pico の 5V 出力は USB 電源から供給されるため、そのまま LED ストリップの電源として使用できます。

【注意事項】
- Raspberry Pi Pico の GPIO は 3.3V の出力となりますが、WS2812 LED ストリップは
  3.3V のデータ信号でも動作する設計になっています。
- Pico と LED ストリップは必ず共通の GND を接続してください。
"""

import rp2
from machine import Pin
import utime

@rp2.asm_pio(
    sideset_init=rp2.PIO.OUT_LOW,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24
)
def ws2812():
    wrap_target()

    # -------------------------------
    # 各ビット送信ループ開始 ("bitloop")
    # -------------------------------
    label("bitloop")
    
    # シフトレジスタから1ビットを取り出し、xレジスタに格納する
    # 同時に、出力ピンをLow(0)に設定
    out(x, 1).side(0)
    
    # xの値が0でなければ（つまり論理1の場合）、
    # 出力ピンをHigh(1)に設定し、2サイクルの遅延を入れた上で
    # 論理0の処理ルーチン"do_zero"へジャンプしない
    jmp(not_x, "do_zero").side(1)[2]
    
    # 【論理1の場合】
    # 出力ピンをHigh(1)のまま2サイクル分遅延（Highパルスの維持）
    nop().side(1)[2]
    
    # その後、出力ピンをLow(0)に戻し、2サイクル分遅延後に次のビット送信へ戻る
    jmp("bitloop").side(0)[2]
    
    # -------------------------------
    # 論理0の場合の処理 ("do_zero")
    # -------------------------------
    label("do_zero")
    
    # 論理0の場合は、出力ピンをLow(0)に維持しながら5サイクル分遅延させる
    nop().side(0)[5]

    wrap()


sm=rp2.StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(0))
sm.active(1)

def write_neopixel(colors):
    for color in colors:
        grb=color[1]<<16 | color[0]<<8 | color[2]
        sm.put(grb,8)

    
NUM_LEDS = 8
# myColor=[0] * NUM_LEDS
myColor=[[100, 0,   0],
         [0,   100, 0],
         [0,   0,   100],
         [0,   100, 100],
         [100, 0,   100],
         [100, 100, 0],
         [200, 100, 0],
         [255, 255, 255]]
write_neopixel(myColor)

utime.sleep(1)
myColor=[[0, 0, 0] for _ in range(NUM_LEDS)]
write_neopixel(myColor)
utime.sleep(0.1)
sm.active(0)
