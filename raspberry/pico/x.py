from picozero import pico_led
from picozero import LED
import time

# pico 本体の LED を点灯します
led = pico_led

led.on()
# 1 秒待機します。
time.sleep(1)
# pico 本体の LED を消灯します
led.off()


