from machine import Pin, I2C  # 入出力モジュール
import ssd1306                # 液晶表示器用ライブラリ
import math                   # 数学関数

# I2C設定 (I2C識別ID 0or1, SDA, SCL)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# 使用するSSD1306のアドレス取得表示（通常は0x3C）
display = i2c.scan()
print( "OLED I2C Address :" + hex(display[0]) )

# ディスプレイ設定（幅, 高さ, 通信仕様）
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# 円描画関数（三角関数を使用）
def circle(x, y, l, color):
    for r in range(360):
        display.pixel(int(x + l * math.cos(math.radians(r))), int(y - l * math.sin(math.radians(r))), color)

# 塗り潰し円描画関数（三角関数を使用）
def fill_circle(x, y, l, color):
    for r in range(360):
        display.line(x, y, int(x + l * math.cos(math.radians(r))), int(y - l * math.sin(math.radians(r))), color)

# 三角描画関数（線で描画）
def triangle(x1, y1, x2, y2, x3, y3, color):
    display.line(x1, y1, x2, y2, color)  # 指定座標から指定座標までの線
    display.line(x2, y2, x3, y3, color)  # 指定座標から指定座標までの線
    display.line(x1, y1, x3, y3, color)  # 指定座標から指定座標までの線

# 塗り潰し三角（正三角形）描画関数（三角関数を使用）
def fill_triangle(x, y, l, color):
    for i in range(int(l/2 * math.tan(math.radians(60)))):
        h = l/2 * math.tan(math.radians(60))  # 高さ
        display.hline(x + math.ceil((i*l/h)/2), y - i, l - math.ceil(i*l/h), color) # 指定座標から塗り潰し三角

# 以下繰り返し
while True:
    # 液晶画面表示内容設定
    display.fill(0) # 表示内容消去
    display.text('SSD1306 TEST', 17, 2, True)  # ('内容', x, y, 色) テキスト表示
    display.hline(0, 12, 128, True)            # (x, y, 長さ, 色) 指定座標から横線
    display.vline(64, 12, 20, True)            # (x, y, 長さ, 色) 指定座標から 縦線
    display.line(0, 32, 128, 32, True)         # (x1, y1, x2, y2, 色) 指定座標1から指定座標2までの線
    display.rect(88, 41, 18, 18, True)         # (x, y, 幅, 高さ, 色)指定座標に四角
    display.fill_rect(109, 41, 18, 18, True)   # (x, y, 幅, 高さ, 色)指定座標に 塗り潰し四角

    # 以下自作関数で描画
    circle(9, 50, 9, True)                 # (x, y, 半径, 色) 円描画関数呼び出し
    fill_circle(31, 50, 9, True)           # (x, y, 半径, 色) 塗り潰し円を描画関数呼び出し
    triangle(42, 58, 52, 42, 62, 58, True) # (x1, y1, x1, y1, x1, y1, 色) 三角描画関数呼び出し
    fill_triangle(65, 58, 20, True)        # (x, y, 底辺長さ, 色) 塗り潰し三角（※正三角形）


    # 設定した内容を表示
    display.show()