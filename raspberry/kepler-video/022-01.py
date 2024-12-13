from lcd1602 import LCD
# https://toptechboy.com/lcd1602-display-library-for-micropython-and-the-raspberry-pi-pico-w/
import utime

lcd = LCD()
while True:
    lcd.write(0, 0, "Helello")
    lcd.write(1, 2, "World")
    utime.sleep(1)


