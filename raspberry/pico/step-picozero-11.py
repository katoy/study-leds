# 配線方法
# ポテンショメータ:
#    +-----------+
#    |   (GND)   |  --- GND
#    |   (OUT)   |  --- GPIO 26 (A0)
#    |  (3.3V)   |  --- 3.3V
#    +-----------+
#

from picozero import Pot # Pot is short for Potentiometer
from time import sleep

dial = Pot(0) # Connected to pin A0 (GP_26)

while True:
    print(dial.value)
    sleep(0.1) # slow down the output

