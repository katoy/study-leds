from gpiozero import LED
from signal import pause
from threading import Timer

# GPIO ピンに接続された LED の設定 (例: GPIO 17)
led = LED(17)

# LED の状態をトグルする関数
def toggle_led():
    led.toggle()  # LED の状態を反転
    # タイマーを使って 0.4 秒後に再び toggle_led を呼び出し
    global timer
    timer = Timer(0.4, toggle_led)
    timer.start()

try:
    # 初回の呼び出し
    toggle_led()

    # プログラムが終了しないように待機
    pause()

except KeyboardInterrupt:
    # Ctrl + C でプログラムが終了する際にここが実行される
    print("\nプログラムを終了します...")

finally:
    # タイマーをキャンセルし、LED をオフにする
    timer.cancel()
    led.off()

