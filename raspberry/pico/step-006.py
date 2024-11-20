# 配線方法：
# [GPIO 17] --- [抵抗] --- (+)LED(-) --- [GND]
# [GPIO 16] --- [ボタン] --- [GND]

from machine import Pin
import time

# 外部 LED を GPIO 17 に接続
led_external = Pin(17, Pin.OUT)

# ボタンを GPIO 16 に接続（プルアップ抵抗を有効化）
button = Pin(16, Pin.IN, Pin.PULL_UP)

try:
    while True:
        if button.value() == 0:  # ボタンが押された場合
            led_external.toggle()  # LED をトグル
            time.sleep(0.5)  # ボタンの押しっぱなしによる連続トグルを防止

        time.sleep(0.1)  # 無駄なループ負荷を軽減

except KeyboardInterrupt:
    # Ctrl + C でプログラムを終了する際にここが実行される
    print("\nプログラムを終了します...")

finally:
    # LED をオフにして終了
    led_external.off()  # LED を消灯
    led_external.init(Pin.IN)  # GPIO ピンを無効化
    print("LED を消灯し、リソースを解放しました。")
