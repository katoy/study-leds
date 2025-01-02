from machine import Pin, I2C
import ssd1306
import math
import utime

def draw_circle(display, cx, cy, radius):
    """
    三角関数を使用して円を描画する
    :param display: SSD1306 のディスプレイオブジェクト
    :param cx: 円の中心 x 座標
    :param cy: 円の中心 y 座標
    :param radius: 円の半径
    """
    for angle in range(0, 360, 1):  # 角度を0度から360度まで1度刻みでループ
        rad = math.radians(angle)
        x = int(cx + radius * math.cos(rad))
        y = int(cy + radius * math.sin(rad))
        display.pixel(x, y, 1)

# I2C 初期化 (ピン番号は適切に変更)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=200000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# 繰り返し計測
repeat_count = 5  # 計測を繰り返す回数
total_time = 0

for i in range(repeat_count):
    # 画面をクリア
    display.fill(0)
    display.show()

    # 計測開始
    start_time = utime.ticks_us()

    # 全ての円を描画
    for r in range(10, 30, 5):  # 半径10から30まで5刻みで描画
        draw_circle(display, 64, 32, r)

    # 表示を更新
    display.show()

    # 計測終了
    end_time = utime.ticks_us()
    elapsed_time = utime.ticks_diff(end_time, start_time)  # 経過時間を計算

    print(f"Iteration {i + 1}: {elapsed_time} us")  # 1回分の描画時間を出力
    total_time += elapsed_time

# 平均時間を計算して出力
average_time = total_time // repeat_count
print(f"Average time: {average_time} us")
