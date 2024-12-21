# See
# https://forums.raspberrypi.com/viewtopic.php?t=300689

# プログラムの概要
# このプログラムは、Raspberry Pi PicoとI2C接続されたSSD1306 OLEDディスプレイを使用して、
# 32x32ピクセルのRaspberry Piロゴをアニメーション表示します。
# ロゴはディスプレイ内で移動し、スクリーン外に出た場合は再び表示範囲内に戻ります。

# 配線方法
# Raspberry Pi PicoとSSD1306 OLEDディスプレイを以下のように接続してください：
# - SDA (OLED) → GP0 (Pico)
# - SCL (OLED) → GP1 (Pico)
# - VCC (OLED) → 3.3V (Pico)
# - GND (OLED) → GND (Pico)

# 依存関係
# - SSD1306ライブラリ（`ssd1306.py` がMicroPython環境にインストールされている必要があります）
# - framebufモジュールは標準ライブラリとして使用できます

# 参考情報
# https://forums.raspberrypi.com/viewtopic.php?t=300689

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

x = 0
y = 0

while True:
    x=(x+5)%WIDTH
    y=(y+3)%HEIGHT
    oled.fill(0)
    oled.blit(fb, x, y)
    oled.blit(fb, x-WIDTH, y)
    oled.blit(fb, x, y-HEIGHT)
    oled.blit(fb, x-WIDTH, y-HEIGHT)
    oled.show()
#    sleep(0.1)
