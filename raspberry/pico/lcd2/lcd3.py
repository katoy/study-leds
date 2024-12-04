"""
Sine Wave Display on SSD1306 OLED with Raspberry Pi Pico

- 機能:
  - I2C 接続で SSD1306 OLED ディスプレイを初期化。
  - サイン波を計算してリアルタイムで描画。

- ハードウェア構成:
  - SDA ピン: GPIO 0
  - SCL ピン: GPIO 1
  - OLED 解像度: 128x64

- 動作:
  角度 0°～500°のサイン波を描画。
"""

import math
import time
from machine import Pin, I2C
import ssd1306

# 定数
OLED_WIDTH = 128
OLED_HEIGHT = 64
CENTER_Y = OLED_HEIGHT // 2  # Y軸の中心
I2C_FREQ = 400000
STEP_ANGLE = 4  # サイン波を描画する角度のステップ

def initialize_oled(sda_pin=0, scl_pin=1):
    """
    SSD1306 OLED を初期化します。
    Args:
        sda_pin (int): SDA ピン番号。
        scl_pin (int): SCL ピン番号。
    Returns:
        SSD1306_I2C: OLED ディスプレイオブジェクト。
    """
    i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=I2C_FREQ)
    return ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

def draw_sine_wave(oled, max_angle=500, step=STEP_ANGLE):
    """
    SSD1306 OLED 上にサイン波を描画します。
    Args:
        oled (SSD1306_I2C): OLED ディスプレイオブジェクト。
        max_angle (int): サイン波を計算する最大角度。
        step (int): サイン波を計算する角度のステップサイズ。
    """
    oled.fill(0)  # 画面クリア
    oled.hline(0, CENTER_Y, OLED_WIDTH, 1)  # 中心線を描画
    x_pos = 0

    for angle in range(0, max_angle, step):
        sine_value = math.sin(math.radians(angle))
        y_pos = CENTER_Y - int(sine_value * (OLED_HEIGHT // 3))  # スケール調整
        oled.pixel(x_pos, y_pos, 1)
        x_pos += 1
        if x_pos >= OLED_WIDTH:  # 幅を超えたら終了
            break
        # time.sleep(0.05)
        oled.show()

# メイン処理
if __name__ == "__main__":
    oled_display = initialize_oled()
    while True:
        draw_sine_wave(oled_display)
        oled_display.fill(0)  # 画面クリア
        
