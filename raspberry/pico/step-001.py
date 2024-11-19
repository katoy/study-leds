from machine import Pin
import time

led = Pin(25, Pin.OUT) # for pico
# led = Pin('LED', Pin.OUT) # for pico w
while True:
    led.toggle()
    time.sleep(1)
    print(led.value())
