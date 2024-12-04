# 3D CUBE MicroPython version with ESP32 and ssd1306 OLED 
# See https://qiita.com/inachi/items/ceb3e8e12022a7cbdf7b

"""
このプログラムは、ESP32 と SSD1306 OLED ディスプレイを使用して、
3D の立方体を回転させて描画するデモを行います。

- 機能:
  - I2C 接続を介して SSD1306 OLED を初期化。
  - 3D 回転アルゴリズムを使用して、立方体の各頂点の座標を計算。
  - 立方体の各辺を OLED ディスプレイに描画。
  - Y軸、X軸、Z軸の順に立方体を回転。

- ハードウェア構成:
  - SDA ピン: GPIO 0
  - SCL ピン: GPIO 1
  - OLED ディスプレイの解像度: 128 x 64

- 使用ライブラリ:
  - `ssd1306` ライブラリ: OLED ディスプレイの制御。
  - `machine` モジュール: I2C と GPIO の制御。
  - `math`    モジュール: 三角関数を使用して座標を計算。

- 動作:
  立方体を 3°ずつ回転させ、OLED ディスプレイに動的に描画します。

- 依存関係:
  - MicroPython 環境。
  - `ssd1306` モジュール。
  - ESP32     マイクロコントローラ。
"""

from machine import Pin, I2C
import ssd1306

from micropython import const
from time import sleep_ms
from math import sin, cos

X = const(64)
Y = const(32)

f = [[0.0 for _ in range(3)] for _ in range(8)]
cube = ((-20,-20, 20), (20,-20, 20), (20,20, 20), (-20,20, 20),
        (-20,-20,-20), (20,-20,-20), (20,20,-20), (-20,20,-20))

# I2C設定 (I2C識別ID 0or1, SDA, SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
oled = ssd1306.SSD1306_I2C(X * 2, Y * 2, i2c)

while True:
    for angle in range(0, 361, 3):  # 0 to 360 deg 3step
        for i in range(8):
            r  = angle * 0.0174532  # 1 degree
            x1 = cube[i][2] * sin(r) + cube[i][0] * cos(r)  # rotate Y
            ya = cube[i][1]
            z1 = cube[i][2] * cos(r) - cube[i][0] * sin(r)
            x2 = x1
            y2 = ya * cos(r) - z1 * sin(r)  # rotate X
            z2 = ya * sin(r) + z1 * cos(r)
            x3 = x2 * cos(r) - y2 * sin(r)  # rotate Z
            y3 = x2 * sin(r) + y2 * cos(r)
            z3 = z2
            x3 = x3 + X
            y3 = y3 + Y
            f[i][0] = x3  # store new values
            f[i][1] = y3
            f[i][2] = z3
        oled.fill(0)  # clear
        oled.line(int(f[0][0]), int(f[0][1]), int(f[1][0]), int(f[1][1]), 1)
        oled.line(int(f[1][0]), int(f[1][1]), int(f[2][0]), int(f[2][1]), 1)
        oled.line(int(f[2][0]), int(f[2][1]), int(f[3][0]), int(f[3][1]), 1)
        oled.line(int(f[3][0]), int(f[3][1]), int(f[0][0]), int(f[0][1]), 1)
        oled.line(int(f[4][0]), int(f[4][1]), int(f[5][0]), int(f[5][1]), 1)
        oled.line(int(f[5][0]), int(f[5][1]), int(f[6][0]), int(f[6][1]), 1)
        oled.line(int(f[6][0]), int(f[6][1]), int(f[7][0]), int(f[7][1]), 1)
        oled.line(int(f[7][0]), int(f[7][1]), int(f[4][0]), int(f[4][1]), 1)
        oled.line(int(f[0][0]), int(f[0][1]), int(f[4][0]), int(f[4][1]), 1)
        oled.line(int(f[1][0]), int(f[1][1]), int(f[5][0]), int(f[5][1]), 1)
        oled.line(int(f[2][0]), int(f[2][1]), int(f[6][0]), int(f[6][1]), 1)
        oled.line(int(f[3][0]), int(f[3][1]), int(f[7][0]), int(f[7][1]), 1)
        oled.line(int(f[1][0]), int(f[1][1]), int(f[3][0]), int(f[3][1]), 1)  # cross
        oled.line(int(f[0][0]), int(f[0][1]), int(f[2][0]), int(f[2][1]), 1)  # cross
        oled.text('3D CUBE', 0, 0)
        oled.show()  # display
        sleep_ms(1)
