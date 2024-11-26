# 配線
# ポテンショメータ:
#    +-----------+
#    |   (GND)   |  --- GND
#    |   (OUT)   |  --- GPIO 26 (A0)
#    |  (3.3V)   |  --- 3.3V
#    +-----------+
# GPIO 17 --- [抵抗] --- (+)LED1(-) --- GND
# GPIO 18 --- [抵抗] --- (+)LED1(-) --- GND
#
# 抵抗（330Ω または 1kΩ）

"""
ポテンショメータで LED の明るさを調整し、明るさがゼロの場合に別の LED を点灯するプログラム。

機能:
1. ポテンショメータを使用して外部 LED の明るさをリアルタイムで制御。
   - ポテンショメータの値に基づき、LED の明るさを 0.0 (消灯) から 1.0 (最大明るさ) まで変化。
2. 外部 LEDの明るさが 0 (ポテンショメータが閾値以下) になると、別の LED を点灯。
   - 明るさがゼロ以外に戻ると、点灯した LED を消灯。
3. コンソールに現在のポテンショメータ値 (LEDの明るさ) を表示。
4. プログラム終了時 (Ctrl+C) にすべての LED を消灯。
"""


from picozero import Pot, PWMLED, LED
from time import sleep

# 定数
POT_PIN = 0          # ポテンショメータのピン (GPIO 26)
LED_PIN = 19         # 明るさ調整用の LED ピン
LED_2_PIN = 17       # 明るさ0時に点灯する LED ピン
BRIGHTNESS_THRESHOLD = 0.05  # 明るさの閾値
SLEEP_TIME = 0.1     # 更新間隔 (秒)

# 初期化
pot = Pot(POT_PIN)            # ポテンショメータ
led = PWMLED(LED_PIN)         # 明るさ調整用 LED
led_2 = LED(LED_2_PIN)        # 明るさ0時に点灯する LED

def update_leds():
    """
    ポテンショメータの値を読み取り、LED の状態を更新します。
    """
    brightness = pot.value  # ポテンショメータの値を取得

    # 明るさが閾値以下の場合は 0 にする
    if brightness <= BRIGHTNESS_THRESHOLD:
        brightness = 0.0

    # LED の明るさを設定
    led.value = brightness

    # 明るさが0のとき、LED_2を点灯
    if brightness == 0:
        led_2.on()
    else:
        led_2.off()

    # 現在の明るさを出力 (デバッグ用)
    print(f"Brightness: {brightness:.2f}")

try:
    print("プログラムを開始します。Ctrl+C で終了します。")
    while True:
        update_leds()  # LEDの状態を更新
        sleep(SLEEP_TIME)
except KeyboardInterrupt:
    # 終了処理
    print("\nプログラムを終了します。")
    led.off()
    led_2.off()
