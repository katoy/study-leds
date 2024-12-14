from machine import Pin, I2C
import ssd1306
import math
import utime

def draw_circle_trig(display, cx, cy, radius):
    """
    三角関数を使用して円を描画する
    :param display: SSD1306 のディスプレイオブジェクト
    :param cx: 円の中心 x 座標
    :param cy: 円の中心 y 座標
    :param radius: 円の半径
    """
    for angle in range(0, 360, 1):  # 角度を 0 度から 360 度まで 1 度刻みでループ
        rad = math.radians(angle)
        x = int(cx + radius * math.cos(rad))
        y = int(cy + radius * math.sin(rad))
        display.pixel(x, y, 1)

def draw_circle_bresenham(display, cx, cy, radius):
    """
    Bresenham のアルゴリズムを使用して円を描画する
    :param display: SSD1306 のディスプレイオブジェクト
    :param cx: 円の中心 x 座標
    :param cy: 円の中心 y 座標
    :param radius: 円の半径
    """
    x = 0
    y = radius
    d = 3 - 2 * radius

    while x <= y:
        # 対称性を利用して 8 つの点を描画
        display.pixel(cx + x, cy + y, 1)
        display.pixel(cx - x, cy + y, 1)
        display.pixel(cx + x, cy - y, 1)
        display.pixel(cx - x, cy - y, 1)
        display.pixel(cx + y, cy + x, 1)
        display.pixel(cx - y, cy + x, 1)
        display.pixel(cx + y, cy - x, 1)
        display.pixel(cx - y, cy - x, 1)

        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1
        x += 1

# I2C 初期化 (ピン番号は適切に変更)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# 繰り返し計測用
repeat_count = 10  # 計測を繰り返す回数

def benchmark_draw_circle():
    total_time_trig = 0
    total_time_bresenham = 0

    for _ in range(repeat_count):
        # 三角関数を使用した描画の計測
        display.fill(0)
        display.show()
        
        start_time = utime.ticks_us()
        for r in range(10, 30, 5):  # 半径 10 から 30 まで 5 刻みで描画
            draw_circle_trig(display, 64, 32, r)
        display.show()
        end_time = utime.ticks_us()
        elapsed_time_trig = utime.ticks_diff(end_time, start_time)
        total_time_trig += elapsed_time_trig
        print(f"Trig method iteration: {elapsed_time_trig} us")

        # Bresenham を使用した描画の計測
        display.fill(0)
        display.show()

        start_time = utime.ticks_us()
        for r in range(10, 30, 5):  # 半径 10 から 30 まで 5 刻みで描画
            draw_circle_bresenham(display, 64, 32, r)
        display.show()
        end_time = utime.ticks_us()
        elapsed_time_bresenham = utime.ticks_diff(end_time, start_time)
        total_time_bresenham += elapsed_time_bresenham
        print(f"Bresenham method iteration: {elapsed_time_bresenham} us")

    # 平均時間の計算
    average_time_trig = total_time_trig // repeat_count
    average_time_bresenham = total_time_bresenham // repeat_count

    print("--------------")
    print(f"Average time (Trig method):      {average_time_trig} us")
    print(f"Average time (Bresenham method): {average_time_bresenham} us")

# ベンチマークを実行
benchmark_draw_circle()
