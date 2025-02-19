from machine import Pin, Timer
import utime

# GPIO ピンの設定
redPin = 15
greenPin = 14
bluePin = 13

redLED = Pin(redPin, Pin.OUT)
greenLED = Pin(greenPin, Pin.OUT)
blueLED = Pin(bluePin, Pin.OUT)

def redBlinker(source):
    redLED.toggle()
def greenBlinker(source):
    greenLED.toggle()
def blueBlinker(source):
    blueLED.toggle()

redTimer = Timer(period=1000, mode=Timer.PERIODIC, callback=redBlinker)
greenTimer = Timer(period=500, mode=Timer.PERIODIC, callback=greenBlinker)
blueTimer = Timer(period=200, mode=Timer.PERIODIC, callback=blueBlinker)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("PRogram Terminated")
    redTimer.deinit()
    greenTimer.deinit()
    blueTimer.deinit()
    redLED.off()
    greenLED.off()
    blueLED.off()
    