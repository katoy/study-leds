"""
ライフゲーム (Conway's Game of Life) を SSD1306 OLED ディスプレイに表示するプログラム

このプログラムの機能:
1. ランダムに初期化されたグリッドを基に、ライフゲームのルールで次世代を計算します。
2. グリッドは上下左右が繋がったトーラス状（円環構造）として扱われます。
   - 画面の上辺と下辺、左辺と右辺が繋がっているものとして次世代を計算します。
3. SSD1306 OLED ディスプレイに現在のグリッドを描画します。
   - ディスプレイの解像度が128x64のため、グリッドサイズを縮小して描画します。
4. 2世代前と同じ状態になった場合、通知を表示し、現在のグリッドをファイルに保存してプログラムを終了します。
5. `grid.txt` が存在する場合、その内容をロードして最初の世代パターンとします。
   - 存在しない場合はランダムなパターンを使用します。
6. プログラムが `Ctrl-C` で終了した際、現在のグリッドをテキストファイルに保存します。
   - 保存ファイル名は日時 (`YYYYMMDD_HHMMSS`) と世代数を含めます。

【配線方法】
本プログラムは、MicroPython環境で動作し、SSD1306 I2C OLEDディスプレイを使用します。
以下のピン配線を参考にしてください。

1. I2C接続:
   - SCL (クロック): ピン GPIO1 (または MicroPython ボードの I2C SCL ピン)
   - SDA (データ): ピン GPIO0 (または MicroPython ボードの I2C SDA ピン)
   - VCC (電源): 3.3V ピン
   - GND (グランド): GND ピン

2. MicroPython I2C初期化:
   - SCL: GPIO1
   - SDA: GPIO0
   - 周波数: 400kHz

3. 使用するディスプレイ:
   - サイズ: 128x64 ピクセル
   - I2C アドレス: 0x3C (一般的な SSD1306 ディスプレイのデフォルトアドレス)

配線が完了したら、このプログラムを実行して動作を確認してください。
"""

import random
import os
from machine import Pin, I2C
import ssd1306
import gc
import utime

def initialize_display():
    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
    return ssd1306.SSD1306_I2C(128, 64, i2c)

def initialize_grid(width, height):
    if "grid.txt" in os.listdir():
        print("Loading grid from grid.txt...")
        with open("grid.txt", "r") as f:
            grid = []
            for line in f:
                row = [1 if char == "█" else 0 for char in line.strip()]
                grid.append(row[:width])
            return grid[:height]
    else:
        print("grid.txt not found. Generating random grid...")
        return [[random.randint(0, 1) for _ in range(width)] for _ in range(height)]

def next_generation(grid, width, height):
    """
    トーラス状のグリッドを考慮して次世代を計算します。
    """
    new_grid = []
    for y in range(height):
        new_row = []
        for x in range(width):
            live_neighbors = sum(
                grid[(y + dy) % height][(x + dx) % width]
                for dy in (-1, 0, 1)
                for dx in (-1, 0, 1)
                if not (dy == 0 and dx == 0)
            )
            if grid[y][x] == 1 and live_neighbors in (2, 3):
                new_row.append(1)
            elif grid[y][x] == 0 and live_neighbors == 3:
                new_row.append(1)
            else:
                new_row.append(0)
        new_grid.append(new_row)
    return new_grid

def draw_grid(display, grid, width, height):
    for y in range(height):
        for x in range(width):
            color = grid[y][x]
            display.pixel(x * 2, y * 2, color)
            display.pixel(x * 2 + 1, y * 2, color)
            display.pixel(x * 2, y * 2 + 1, color)
            display.pixel(x * 2 + 1, y * 2 + 1, color)
    display.show()

def save_grid_to_file(grid, generation):
    try:
        current_time = utime.localtime()
        timestamp = "{:04d}{:02d}{:02d}_{:02d}{:02d}{:02d}".format(
            current_time[0], current_time[1], current_time[2],
            current_time[3], current_time[4], current_time[5]
        )
        filename = f"grid_{timestamp}_gen{generation}.txt"
        with open(filename, "w") as f:
            for row in grid:
                line = "".join("█" if cell else " " for cell in row)
                f.write(line + "\n")
        print(f"Grid saved to {filename}")
    except Exception as e:
        print(f"An error occurred while saving the grid: {e}")

def main():
    width, height = 64, 32
    display = initialize_display()
    grid = initialize_grid(width, height)
    generation = 0
    previous_grid, two_generations_ago = None, None

    try:
        while True:
            draw_grid(display, grid, width, height)
            if two_generations_ago == grid:
                print("No change from two generations ago! Saving grid and exiting...")
                save_grid_to_file(grid, generation)
                break
            two_generations_ago = previous_grid
            previous_grid = grid
            grid = next_generation(grid, width, height)
            generation += 1
            # utime.sleep(0.1)
    except KeyboardInterrupt:
        print("\nCtrl-C detected, exiting...")
    finally:
        print("Exiting program safely.")

if __name__ == "__main__":
    main()
