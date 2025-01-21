import machine
import utime

servoPin = 15
servo = machine.PWM(machine.Pin(servoPin))
servo.freq(50)

while True:
    angle = int(input('What angle do you desire? '))
    writeVal = 6553 / 180 * angle + 1638
    servo.duty_u16(int(writeVal))
    utime.sleep(0.5)
