from machine import Pin, I2C
import ssd1306
import math
import utime

def draw_fig(display, cx, cy, radius, cycle_x, cycle_y, phase_angle):
    """
    アニメーション用に三角関数を使用して楕円状の図形を描画する。
    各ピクセルを計算して描画する際、x方向とy方向に異なる周期と位相を適用する。
    :param display: SSD1306 のディスプレイオブジェクト
    :param cx: 楕円の中心 x 座標
    :param cy: 楕円の中心 y 座標
    :param radius: 楕円の基準となる半径
    :param cycle_x: x方向の変化の周期
    :param cycle_y: y方向の変化の周期
    :param phase_angle: 現在の位相角 (度単位)
    """
    phase_rad = math.radians(phase_angle)  # 位相角をラジアンに変換
    for angle in range(0, 360, 1):  # 楕円の輪郭を描くために0度から360度までループ
        rad = math.radians(angle)  # 現在の角度をラジアンに変換
        # x方向とy方向の位置を計算（楕円の周期と位相を適用）
        x = int(cx + radius * math.cos(cycle_x * rad + phase_rad))
        y = int(cy + radius * math.sin(cycle_y * rad) / 2)  # y方向は高さを半分に調整
        # ピクセルを描画
        display.pixel(x, y, 1)

# I2C 初期化 (ピン番号は適切に変更)
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)  # SDA: GPIO0, SCL: GPIO1
display = ssd1306.SSD1306_I2C(128, 64, i2c)  # 解像度128x64のSSD1306を使用

# 描画の中心座標と半径の設定
center_x, center_y = [64, 40]  # ディスプレイの中心を基準に設定
radius = 40  # 楕円の半径（基準値）

# アニメーションのループ
while True:
    # 周期の組み合わせを順に適用
    for [cycle_x, cycle_y] in [
            [1, 1],
            [1, 2], [1, 1.5], [2, 3],
            [2, 1],
            [2, 5],
            [5, 2],
        ]:
        # 位相角を変化させてアニメーション効果を作成
        for phase_angle in range(0, 360, 5):  # 位相角を5度刻みで変化
            # 画面をクリア
            display.fill(0)
            # 現在の周期情報をディスプレイに表示
            display.text(f"x={cycle_x}, y={cycle_y}", 0, 0, 1)
            # 図形を描画
            draw_fig(display, center_x, center_y, radius, cycle_x, cycle_y, phase_angle)
            # 描画をディスプレイに反映
            display.show()
            # 短い遅延を入れてアニメーションを滑らかに
            utime.sleep(0.1)
