from machine import Pin
import utime
import _thread

# ピンの設定
greenPin = 14
redPin = 15

greenLED = Pin(greenPin, Pin.OUT)
redLED = Pin(redPin, Pin.OUT)

# 点灯・消灯時間
greenOn = 0.5
greenOff = 0.5
redOn = 1
redOff = 1

# スレッドとメインループの終了フラグ
running = True

# スレッド同期用ロック
sync_lock = _thread.allocate_lock()
sync_lock.acquire()  # 最初はロック状態にする

# スレッド用 LED 点滅関数
def led_blink_thread(led, led_on, led_off):
    global running
    sync_lock.acquire()  # ロックが解放されるのを待つ
    sync_lock.release()

    while running:
        led.value(1)
        utime.sleep(led_on)
        led.value(0)
        utime.sleep(led_off)

    led.value(0)  # スレッド終了時に LED を消灯

# メインスレッド用 LED 点滅関数
def led_blink_main(led, led_on, led_off):
    global running
    while running:
        led.value(1)
        utime.sleep(led_on)
        led.value(0)
        utime.sleep(led_off)

# スレッドを起動
_thread.start_new_thread(led_blink_thread, (redLED, redOn, redOff))

# メインスレッド用処理
try:
    sync_lock.release()  # スレッドの開始を許可
    led_blink_main(greenLED, greenOn, greenOff)  # メインスレッドで LED 点滅処理を実行
except KeyboardInterrupt:
    # Ctrl-C で停止
    print("Stopping...")
    running = False  # 終了フラグを設定
    utime.sleep(1)   # スレッドの終了を待つ
finally:
    # プログラム終了時にすべての LED を消灯
    greenLED.value(0)
    redLED.value(0)
    print("LEDs turned off. Program stopped.")
