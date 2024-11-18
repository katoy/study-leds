from picozero import Button
from time import sleep

button = Button(16)

while True:
    if button.is_pressed:
        print("Button is pressed")
    sleep(0.1)