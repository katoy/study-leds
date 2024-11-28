# 配線
# LCD 1602                Raspberry Pi Pico
# +---------+             +-----------------+
# | GND     | ----------- | GND             |
# | VCC     | ----------- | 3.3V (または 5V) |
# | SDA     | ----------- | GPIO 0 (I2C SDA)|
# | SCL     | ----------- | GPIO 1 (I2C SCL)|
# +---------+             +-----------------+

import time
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd


I2C_ADDR     = 0x3f
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

lcd.putstr("It Works!\nSecond Line")
time.sleep(3)

lcd.clear()
lcd.putstr("Hello\nI'm METAELE")
time.sleep(3)

lcd.clear()
lcd.putchar(chr(247))
time.sleep(3)

lcd.clear()
heart = bytearray([0x00,0x0a,0x1f,0x1f,0x0e,0x04,0x00,0x00])
lcd.custom_char(0, heart)
lcd.putstr("Hello from\n"+chr(0)+" peppe8o.com "+chr(0))
time.sleep(3)

lcd.backlight_off()
