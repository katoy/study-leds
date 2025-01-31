from rgbled import *
import utime

redPin = 15
greenPin = 14
bluePin = 13

myLED = RGBLED(redPin, greenPin, bluePin)

try:
    while True:
        myColor = input("What color? ")
        myColor = myColor.lower()
        if myColor not in myLED.NORMALIZED_COLORS:
            print("invalid color name")
        else:
            myLED.set_color(myColor)
            utime.sleep(1)

except KeyboardInterrupt:
    myLED.off()
    print("Origran has terminated")