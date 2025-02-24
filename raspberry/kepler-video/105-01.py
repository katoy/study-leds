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
    sideset_init=rp2.PIO.OUT_HIGH,
    out_shiftdir=rp2.PIO.SHIFT_LEFT,
    autopull=True,
    pull_thresh=24
)
def ws2812():
    wrap_target()
    
    # 各ビットを送信するループの開始
    label('bitloop')
    
    # シフトレジスタから1ビットを取り出し、x レジスタに格納
    # 同時に、出力ピンを Low (0) に設定
    out(x, 1).side(0)
    
    # x レジスタの値が 0 でなければ、次の命令をスキップせずに実行（論理1の場合）
    # この命令で出力ピンを High (1) に設定し、x の値が 0 なら 'do_zero' ラベルへジャンプ（論理0の場合）
    jmp(not_x, 'do_zero').side(1)
    
    # 論理1の場合の High 信号維持:
    # nop 命令で何もしないが、side-set により出力ピンは High のままで、
    # [5-1] で 4 サイクル分の遅延を発生させる
    nop().side(1)[5-1]
    
    # 論理1の場合の Low 信号維持:
    # 出力ピンを Low に設定し、[2-1] で 1 サイクル分の遅延を入れる
    nop().side(0)[2-1]
    
    # 次のビット送信のためにループの先頭へジャンプし、出力ピンを Low に保持
    jmp('bitloop').side(0)
    
    # 論理0の場合の処理開始
    label('do_zero')
    
    # 論理0の場合の High 信号維持:
    # 出力ピンを High に設定し、[2-1] で 1 サイクル分の遅延を入れる
    nop().side(1)[2-1]
    
    # 論理0の場合の Low 信号維持:
    # 出力ピンを Low に設定し、[6-1] で 5 サイクル分の遅延を入れた後、
    # 次のビット送信のためにループの先頭へジャンプ
    jmp('bitloop').side(0)[6-1]

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
