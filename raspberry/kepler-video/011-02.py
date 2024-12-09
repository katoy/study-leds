from picozero import Pot, PWMLED
import utime

# 初期設定
pot = Pot(28)     # ポテンショメータ (GPIO28)
led = PWMLED(15)  # PWM対応LED (GPIO15)

while True:
    # ポテンショメータの値 (0.0 〜 1.0) を取得して LED の明るさを設定
    brightness = pot.value
    led.value = brightness

    print(f"Pot Value: {brightness:.4f}, LED Brightness: {led.value:.4f}")
    utime.sleep(0.1)
