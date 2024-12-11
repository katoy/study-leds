"""
RGB LED の明るさを個別に調整するプログラム

機能:
1. 各ポテンショメータの値 (0.0〜1.0) を読み取り、対応するRGB LEDの明るさを調整します。
2. 非線形スケーリング (対数的な感覚に近い明るさ制御) を適用。
3. 各RGB LEDは独立したポテンショメータで制御されます。

設定:
- GPIO26: 赤色LED用ポテンショメータ
- GPIO27: 緑色LED用ポテンショメータ
- GPIO28: 青色LED用ポテンショメータ
- GPIO13: 赤色PWM LED
- GPIO12: 緑色PWM LED
- GPIO11: 青色PWM LED

使用ライブラリ:
- picozero: 簡単なハードウェア制御のためのMicroPythonライブラリ
- math: 非線形スケーリングに使用
"""

from picozero import Pot, PWMLED
import utime
import math

# 定数
MAX_BRIGHTNESS = math.pow(2, 16)  # 最大明るさ
SCALING_STEPS = 100               # 明るさ調整のステップ数
SCALING_FACTOR = math.pow(MAX_BRIGHTNESS, 1 / SCALING_STEPS)  # スケーリング係数

# RGB LED の設定
led_config = [
    {"pot": Pot(26), "led": PWMLED(13)},  # 赤色
    {"pot": Pot(27), "led": PWMLED(12)},  # 緑色
    {"pot": Pot(28), "led": PWMLED(11)},  # 青色
]

def scale_value(value, scaling_factor, max_brightness):
    """
    ポテンショメータの値 (0.0〜1.0) を非線形スケーリングし、LEDの明るさに変換。
    """
    return math.pow(scaling_factor, value * SCALING_STEPS) / max_brightness

while True:
    for config in led_config:
        pot = config["pot"]
        led = config["led"]

        # ポテンショメータの値を取得し、スケーリング
        val = pot.value
        scaled_val = scale_value(val, SCALING_FACTOR, MAX_BRIGHTNESS)

        # LED の明るさを設定
        led.value = scaled_val

        # デバッグ用出力
        print(f"Pot Value: {val:.2f}, Scaled Value: {scaled_val:.4f}, LED: {led.value:.4f}")

    # 0.1秒待機
    utime.sleep(0.1)
