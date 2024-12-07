from picozero import pico_led, LED, DigitalLED
import utime

# 内蔵 LED (次の指定のいずれかを使う)
led = pico_led
# led = LED("LED", pwm=False)
# led = DigitalLED("LED")

# 短い感覚でのブリンクを 5 回繰り返す
led.blink(on_time=0.2, off_time=0.2, n=5, wait=True)

# 長い感覚でのブリンクを 5 回繰り返す
led.blink(on_time=1, off_time=2, n=5, wait=True)
