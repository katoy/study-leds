import machine
import utime
import math

vPin = 27
hPin = 26

vJoy = machine.ADC(vPin)
hJoy = machine.ADC(hPin)

while True:
    vVal = vJoy.read_u16()
    hVal = hJoy.read_u16()

    vCal = int(0.00306 * vVal - 100.766)
    hCal = int(0.00306 * hVal - 100.766)
    mag = math.sqrt(vCal ** 2 + hCal ** 2)
    if mag < 6:
        hCal = 0
        vCal = 0

    deg = math.atan2(hCal, vCal) / 2 / math.pi * 360
    print(deg)
    utime.sleep(0.2)


