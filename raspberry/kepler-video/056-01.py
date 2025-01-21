import machine
import utime
import math

xPin = 27
yPin = 26

xJoy = machine.ADC(xPin)
yJoy = machine.ADC(yPin)

while True:
    xVal = xJoy.read_u16()
    yVal = yJoy.read_u16()
    print(xVal, yVal)
    utime.sleep(0.25)
