from machine import Pin
import time

led = Pin(25, Pin.OUT) # for pico
while True:
    led.toggle()
    time.sleep(1)
    print(led.value())
