from machine import Pin
from machine import Timer
import utime

redPin = 15
greenPin = 14
bluePin = 13

redLED = Pin(redPin, Pin.OUT)
greenLED = Pin(greenPin, Pin.OUT)
blueLED = Pin(bluePin, Pin.OUT)

def redBlinker(source):
    redLED.toggle()
    redOff = Timer(period=100, mode=Timer.ONE_SHOT, callback=turnRedOff)
def turnRedOff(source):
    redLED.off()

def greenBlinker(source):
    greenLED.toggle()
    
def blueBlinker(source):
    blueLED.toggle()

redTime = Timer(period=1000, mode=Timer.PERIODIC, callback=redBlinker)
greenTime = Timer(period=1000, mode=Timer.PERIODIC, callback=greenBlinker)
blueTime = Timer(period=4000, mode=Timer.PERIODIC, callback=blueBlinker)

x = 0
try:
    while True:
        print(x)
        utime.sleep(1)
        x = x + 1
except KeyboardInterrupt:
    redTime.deinit()
    greenTime.deinit()
    blueTime.deinit()
    
    redLED.off()
    greenLED.off()
    blueLED.off()
    
    
    