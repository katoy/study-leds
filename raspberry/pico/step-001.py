from led_control import Pico_LED
import time

led = Pico_LED()  # Pico_LED インスタンスを作成

try:
    # LED を点滅させる
    while True:
        led.toggle()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("ユーザーによる中断が発生しました。")
finally:
    led.cleanup()
    print("プログラムを終了しました。")

