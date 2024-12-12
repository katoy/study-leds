from picozero import Button
import utime

# 初期設定
botton = Button(14, pull_up=True) # プッシュボtん (GPIO4)

while True:
    print(f"Button is_pressed: {botton.is_pressed}")
    utime.sleep(0.1)

