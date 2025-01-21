import machine
from ws2812 import WS2812
import utime


ws = WS2812(machine.Pin(0), 8)

ws[0] = [64, 154, 227]
ws[1] = [128, 0, 128]
ws[2] = [50, 150, 50]
ws[3] = [255, 30, 30]
ws[4] = [0, 128, 255]
ws[5] = [99, 199, 0]
ws[6] = [128, 128, 128]
ws[7] = [255, 100, 0]
ws.write()
utime.sleep(2)

ws[0] = [0, 0, 0]
ws[1] = [0, 0, 0]
ws[2] = [0, 0, 0]
ws[3] = [0, 0, 0]
ws[4] = [0, 0, 0]
ws[5] = [0, 0, 0]
ws[6] = [0, 0, 0]
ws[7] = [0, 0, 0]
ws.write()


