from imu import MPU6050
from ssd1306 import SSD1306_I2C
from machine import I2C, Pin
import math
import utime

# 定数定義
I2C0_SDA_PIN = 16
I2C0_SCL_PIN = 17
I2C1_SDA_PIN = 2
I2C1_SCL_PIN = 3
I2C_FREQ = 400000

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
CENTER_X = DISPLAY_WIDTH // 2
CENTER_Y = 39  # ナビゲーションの中心Y位置

# 初期化
i2c = I2C(0, sda=Pin(I2C0_SDA_PIN), scl=Pin(I2C0_SCL_PIN), freq=I2C_FREQ)
mpu = MPU6050(i2c)
i2c2 = I2C(1, sda=Pin(I2C1_SDA_PIN), scl=Pin(I2C1_SCL_PIN), freq=I2C_FREQ)
disp = SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c2)

# 角度調整
def adjust_angle(degree):
    if degree > 170:
        degree -= 360
    elif degree < -180:
        degree += 360
    return degree

# 円を描画
def draw_circle(radius, cx, cy, orgx, orgy):
    for deg in range(0, 360, 15):
        rad = math.radians(deg)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        disp.pixel(int(cx + x + orgx), int(cy + y + orgy), 1)

# ナビゲーションの描画
def draw_nav(pitch, roll):
    disp.rect(0, 14, DISPLAY_WIDTH, 50, 1)
    disp.hline(0, CENTER_Y, DISPLAY_WIDTH, 1)
    disp.vline(CENTER_X, 14, 64, 1)
    cx = pitch / 180 * 64
    cy = roll / 180 * 25
    draw_circle(6, cx, cy, CENTER_X, CENTER_Y)

# IMUデータの更新
def update_imu_data(delta_time, roll_g, pitch_g, roll_comp, pitch_comp, roll_error, pitch_error):
    x_gyro = mpu.gyro.x
    y_gyro = -mpu.gyro.y
    z_gyro = mpu.gyro.z

    x_accel = mpu.accel.x
    y_accel = mpu.accel.y
    z_accel = mpu.accel.z

    roll_g += y_gyro * delta_time
    pitch_g += x_gyro * delta_time

    roll_a = math.degrees(math.atan(x_accel / z_accel)) + roll_error * 0.05
    pitch_a = math.degrees(math.atan(y_accel / z_accel)) + pitch_error * 0.05

    roll_comp = roll_a * 0.005 + 0.995 * (roll_comp + y_gyro * delta_time)
    pitch_comp = pitch_a * 0.005 + 0.995 * (pitch_comp + x_gyro * delta_time)

    roll_error += (roll_a - roll_comp) * delta_time
    pitch_error += (pitch_a - pitch_comp) * delta_time

    return roll_g, pitch_g, roll_comp, pitch_comp, roll_error, pitch_error

# メインループ
def main():
    roll_g = pitch_g = 0
    roll_comp = pitch_comp = 0
    roll_error = pitch_error = 0
    delta_time = 0
    count = 10

    while True:
        t_start = utime.ticks_ms()

        # IMUデータ更新
        roll_g, pitch_g, roll_comp, pitch_comp, roll_error, pitch_error = update_imu_data(
            delta_time, roll_g, pitch_g, roll_comp, pitch_comp, roll_error, pitch_error
        )

        # ディスプレイ更新
        count -= 1
        if count <= 0:
            count = 10
            # print(f"RA: {roll_g:.2f}, PA: {pitch_g:.2f}, RC: {roll_comp:.2f}, PC: {pitch_comp:.2f}")
            print(f"RC: {roll_comp:.2f}, PC: {pitch_comp:.2f}")


            disp.fill(0)
            message = f"P:{pitch_comp:.1f} R:{roll_comp:.1f}"
            disp.text(message, 0, 0)
            draw_nav(pitch_comp, roll_comp)
            disp.show()

        t_stop = utime.ticks_ms()
        delta_time = (t_stop - t_start) * 0.001

# 実行
if __name__ == "__main__":
    main()
