# See
# https://forums.raspberrypi.com/viewtopic.php?t=300689

# プログラムの概要
# このプログラムは、MicroPythonを使用してSSD1306 OLEDディスプレイに画像やテキストを描画します。
# ラズベリーパイのロゴと独自のパターンを表示する機能を備えています。

# 機能
# - SSD1306 OLEDディスプレイに接続し、I2Cアドレスを確認。
# - ラズベリーパイのロゴを表示。
# - カスタムグリッドパターンを生成してアニメーション表示。
# - 各パターンを1秒間表示し、最後に数秒間停止。

# 配線方法
# - 使用デバイス: Raspberry Pi Pico
# - 接続:
#   - SSD1306のSCLピンをPicoのGP1ピンに接続。
#   - SSD1306のSDAピンをPicoのGP0ピンに接続。
#   - SSD1306のVCCピンを3.3Vに接続。
#   - SSD1306のGNDピンをGNDに接続。
# - 注意:
#   - デフォルトのI2Cバス (I2C0) を使用しています。
#   - ピン番号は環境に応じて変更してください。
#   - 接続後にI2Cアドレスが正しいか確認してください。

# Display Image & text on I2C driven ssd1306 OLED display 
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
from time import sleep

WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height

i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config


oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display

# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

# Load the raspberry pi logo into the framebuffer (the image is 32x32)
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)

def sq(x, y):
    oled.rect(7*x,7*y,8,8,1)

def pc(x, y):
    oled.rect(7*x+3,7*y+3,2,2,1)

def draw(b):
    p2=1

    oled.fill(0)
    oled.blit(fb, 96, 0)

    for y in range(3):
        for x in range(3):
           sq(3+x,y)
           if (b & p2):
               pc(3+x,y)
           p2<<=1

    for y in range(3):
        for x in range(8):
           sq(1+x,3+y)
           if (b & p2):
               pc(1+x,3+y)
           p2<<=1

    for y in range(2):
        for x in range(3):
           sq(3+x,6+y)
           if (b & p2):
               pc(3+x,6+y)
           p2<<=1

    oled.show()


B=[0x7fffefffff,
0x7fffffef7f,
0x7fffffefed,
0x7ffffff3ed,
0x7ffffffba5,
0x7ffffffa65,
0x7ffffffb41,
0x7ffffff309,
0x7ffffff340,
0x7fffffd260,
0x7fffff3260,
0x7fffff0a60,
0x7ffbfb0e60,
0x7ffbfb1260,
0x7ffbeb02e0,
0x7ffbeb0320,
0x7ffbeb2200,
0x7fe7eb2200,
0x7fe9eb2200,
0x7febe92000,
0x7faba96000,
0x7faba98000,
0x7faba84000,
0x7faa684000,
0x7fea280000,
0x7f9a280000,
0x7f86280000,
0x7f88280000,
0x7e48280000,
0x3668280000,
0x3e48080000,
0x4e48080000,
0x0668080000,
0x0618080000,
0x0208180000,
0x0208040000,
0x00000c0000,
0x0000100000]

while True:
    for b in B:
        draw(b)
        sleep(1)

    sleep(4)
