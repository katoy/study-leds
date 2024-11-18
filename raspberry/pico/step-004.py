from machine import Pin, Timer
import time

# GPIO ピンに接続されたLEDの設定（例: GPIO 17 と GPIO 16）
led1 = Pin(17, Pin.OUT)  # 1つ目の LED
led2 = Pin(16, Pin.OUT)  # 2つ目の LED

# タイマーの設定
timer1 = Timer()
timer2 = Timer()

# LED 1 の状態をトグルする関数
def toggle_led1(timer):
    led1.value(not led1.value())  # LEDの状態を反転

# LED 2 の状態をトグルする関数
def toggle_led2(timer):
    led2.value(not led2.value())  # LEDの状態を反転

# タイマーを使って LED の点滅を設定
timer1.init(period=500, mode=Timer.PERIODIC, callback=toggle_led1)  # 0.5 秒 (2Hz)
timer2.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led2)  # 1 秒 (1Hz)

try:
    # プログラムが終了しないように無限ループで待機
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Ctrl + C でプログラムを終了する際にここが実行される
    print("\nプログラムを終了します...")

finally:
    # タイマーを停止し、LED をオフにする
    timer1.deinit()
    timer2.deinit()
    led1.value(0)
    led2.value(0)

