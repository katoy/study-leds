from machine import Pin
import utime
from dht import DHT11

pin = Pin(16, Pin.OUT, Pin.PULL_DOWN)
         
sensor = DHT11(pin)
         
while True:
    sensor.measure()
    tempC = sensor.temperature()
    hum = sensor.humidity()
    print(tempC, hum)
    utime.sleep(2)
