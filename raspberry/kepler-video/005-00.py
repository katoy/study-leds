import machine
import time

potentiometer = machine.ADC(28)
while True:
    value = potentiometer.read_u16()
    voltage = 3.3 * (value - 80.0) / (65535.0 - 80.0)
    print(voltage, value)
    time.sleep(0.5)
