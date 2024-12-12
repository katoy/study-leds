"""
プッシュボタンを使って LED の状態を切り替えるプログラム

【プログラムの機能】
1. プッシュボタン (GPIO14) を押すたびに、LED (GPIO13) の点灯/消灯状態を切り替えます (トグル動作)。
2. ボタンが押されている間はループを待機し、ノイズによる誤作動を防止します。

【配線方法】
1. プッシュボタン:
   - 一端を GPIO14 に接続
   - もう一端を GND に接続 (プルアップ設定)
2. LED:
   - アノード (長い端子) を GPIO13 に接続
   - カソード (短い端子) を抵抗を介して GND に接続
"""

from picozero import Button, LED
import utime

# 初期設定
button = Button(14, pull_up=True)  # プッシュボタン (GPIO14)
led = LED(13)                      # LED (GPIO13)

# LEDを初期状態でオフに設定
led.off()

while True:
    # ボタンが押された場合、LED の状態を切り替える
    if button.is_pressed:
        led.toggle()

    # ボタンが押され続けている間は待機
    while button.is_pressed:
        utime.sleep(0.1)

    # ボタンの連続押しを防ぐための待機
    utime.sleep(0.1)
