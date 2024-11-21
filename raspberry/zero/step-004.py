# 配線
# GPIO 17 --- [アノード (+)]LED[カソード (-)] --- [抵抗] --- GND
# GPIO 27 --- [アノード (+)]LED[カソード (-)] --- [抵抗] --- GND
#
# 抵抗（330Ω ～ 1kΩ)
#

from gpiozero import LED
from signal import pause
from threading import Timer

# GPIO ピンに接続されたLEDの設定（例: GPIO 17 と GPIO 27）
led1 = LED(17)  # 1 つ目の LED
led2 = LED(27)  # 2 つ目の LED

# LED 1 の状態をトグルする関数
def toggle_led1():
    led1.toggle()  # LED 1 の状態を反転
    global timer1
    timer1 = Timer(0.5, toggle_led1)  # 0.5 秒（2 Hz）で点滅
    timer1.start()

# LED 2 の状態をトグルする関数
def toggle_led2():
    led2.toggle()  # LED 2 の状態を反転
    global timer2
    timer2 = Timer(1.0, toggle_led2)  # 1 秒（1 Hz）で点滅
    timer2.start()

try:
    # LED の点滅を開始
    toggle_led1()
    toggle_led2()

    # プログラムが終了しないように待機
    pause()

except KeyboardInterrupt:
    # Ctrl + C でプログラムが終了する際にここが実行される
    print("\nプログラムを終了します...")

finally:
    # タイマーをキャンセルし、LED をオフにする
    timer1.cancel()
    timer2.cancel()
    led1.off()
    led2.off()
