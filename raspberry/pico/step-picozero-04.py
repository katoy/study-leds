from picozero import Button
from time import sleep

# 内部プルアップ抵抗が picozero.Button で自動的に有効になる
button = Button(16)

while True:
    if button.is_pressed:
        print("Button is pressed")
    sleep(0.1)

