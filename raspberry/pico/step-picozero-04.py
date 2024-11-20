# 配線方法
# [GPIO 16] --- [ボタン] --- [GND]

from picozero import Button
from time import sleep

button = Button(16, pull_up=True)  # 内部プルアップ抵抗を有効化

while True:
    if button.is_pressed:
        print("Button is pressed")
    sleep(0.2)
