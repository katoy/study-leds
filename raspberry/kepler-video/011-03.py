from picozero import Pot, PWMLED
import utime
import math

# 定数の設定
PWM_LED_PIN = 15        # PWM 対応 LED のピン番号
POTENTIOMETER_PIN = 28  # ポテンショメータのピン番号
C = math.pow(math.pow(2, 16), 1/100)  # 2^16 の 100 乗根

# デバイスの初期化
pot = Pot(POTENTIOMETER_PIN)  # GPIO28 に接続されたポテンショメータ
led = PWMLED(PWM_LED_PIN)     # GPIO15 に接続された PWM対応LED

while True:
    # ポテンショメータの値 (0.0 〜 1.0) を取得
    pot_val = pot.value  # 0 〜 1 の値
    scaled_val = math.pow(C, pot_val * 100)  # ポテンショメータ値を指数関数でスケール
    led_brightness = scaled_val / math.pow(2, 16)  # 最大値を2^16で正規化
    led.value = led_brightness  # LEDの明るさを設定 (0 〜 1)

    # デバッグ用出力
    print(f"Pot Value: {pot_val:.4f}, Scaled Value: {scaled_val:.4f}, LED Brightness: {led_brightness:.4f}")

    utime.sleep(0.1)
