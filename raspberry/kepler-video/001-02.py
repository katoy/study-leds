from picozero import pico_led, LED, DigitalLED
import utime

# 内蔵 LED (次の指定のいずれかを使う)
led = pico_led
# led = LED("LED", pwm=False)
# led = DigitalLED("LED")

while True:
    led.toggle()
    utime.sleep(1)
