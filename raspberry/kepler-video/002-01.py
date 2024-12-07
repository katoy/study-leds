from picozero import pico_led, LED, DigitalLED
import utime

# 外部 LED を使う場合の指定
led = LED(15)

while True:
    led.on()
    utime.sleep(1)
    led.off()
    utime.sleep(1)
