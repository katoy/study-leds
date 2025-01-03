"""
プッシュボタンを使って LED の状態を切り替えるプログラム

【プログラムの機能】
1. プッシュボタン (GPIO14) を押すたびに、LED (GPIO13) の点灯/消灯状態を切り替えます (トグル動作)。
2. ボタンが押されている間は何もせず、押された瞬間にのみ処理を実行します。

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

# ボタンの現在の状態を追跡する変数
button_was_released = True

while True:
    # ボタンが押された場合（前回が離された状態で、今回が押された状態になるとき）
    if button.is_pressed and button_was_released:
        led.toggle()                # LEDの状態を切り替える
        button_was_released = False  # ボタンが押されたことを記録

    # ボタンが離された場合
    if not button.is_pressed:
        button_was_released = True  # ボタンが離されたことを記録

    # 短い遅延を入れる
    utime.sleep(0.05)
