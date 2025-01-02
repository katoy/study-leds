# See https://water2litter.net/rum/post/python_lissajous2/

from machine import Pin, I2C
import ssd1306
import math
import time

# I2C設定（ピン番号は環境に合わせて変更してください）
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=200000)  # SDA: GPIO2, SCL: GPIO3
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# リサージュ曲線のパラメータ
theta_max = 2 * math.pi
theta_steps = 201
delta_steps = 51
delta_theta = [2 * math.pi * i / delta_steps for i in range(delta_steps)]
theta_values = [theta_max * i / (theta_steps - 1) for i in range(theta_steps)]
a = 3 # 1 2 3
b = 2 # 1 2 3

# 描画ループ
while True:
    for delta in delta_theta:
        oled.fill(0)  # 画面クリア
        for theta in theta_values:
            # 座標計算 (128x64 画面に合わせてスケール)
            x = int((math.cos(a * theta) + 1) * 63)  # 0 - 127 の範囲にスケール
            y = int((math.sin(b * theta + delta) + 1) * 31)  # 0 - 63 の範囲にスケール
            oled.pixel(x, y, 1)  # 点を描画
        oled.show()  # 画面に反映
        time.sleep(0.01)  # 短い待ち時間

