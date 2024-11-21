# 配線鳳凰
# GPIO 17 --- [抵抗] --- (+)LED1(-) --- GND
#
# 抵抗（330Ω または 1kΩ）

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

# pico GPIO 17 の LED を点灯します
led = LED(17)
led.on()
time.sleep(1)
led.off()

led = LED(25)  # GPIO 25 は内蔵 LED
led.on()
time.sleep(1)
led.off()
