import machine
from ws2812 import WS2812
import utime

pixSize = 8
interval = 0.1
ws = WS2812(machine.Pin(0), pixSize)

red = [255, 0, 0]
green = [0, 255, 0]

rg = [range(0, pixSize, 1), range(pixSize - 1, 0, -1)]
while True:
    for r in rg:
        for i in r:
            for p in range(pixSize):
                ws[p] = red
            ws[i] = green
            ws.write()
            utime.sleep(interval)
            


