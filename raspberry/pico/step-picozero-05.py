from picozero import Button
from time import sleep

# ボタンを GPIO16 に接続
button = Button(16)

# ボタンが押されたときに呼び出される関数
def button_pressed():
    print("Button is pressed!")

# ボタンが話されたときに呼び出される関数
def button_released():
    print("Button is released!")

# 割り込みの設定
button.when_pressed = button_pressed
button.when_released = button_released

# メインループ（割り込みを待機）
while True:
    sleep(0.1)  # 必要に応じて他のタスクを実行
