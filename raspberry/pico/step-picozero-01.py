from picozero import pico_led
import time

# pico w 本体のLEDを点灯します
pico_led.on()

# 1秒待機します。
time.sleep(1)

# pico w 本体のLEDを消灯します
pico_led.off()
