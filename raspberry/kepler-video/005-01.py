from picozero import Pot
import time

potentiometer = Pot(28)
while True:
    voltage = potentiometer.value * 3.3
    print(voltage)
    time.sleep(0.5)
