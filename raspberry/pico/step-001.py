from machine import Pin
import time

led = Pin(25, Pin.OUT)
while True:
    led.on()
    time.sleep(1)
    led.off()
    time.sleep(1)
