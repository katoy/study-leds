from machine import Pin, ADC, PWM
import utime

pot = ADC(28)
led = PWM(Pin(15))

led.freq(1000)
led.duty_u16(0)

while True:
    potVal = pot.read_u16()
    led.duty_u16(potVal)
    utime.sleep(0.1)
