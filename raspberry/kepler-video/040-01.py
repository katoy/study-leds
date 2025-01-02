from imu import MPU6050
from ssd1306 import SSD1306_I2C
from machine import I2C, Pin
import math
import utime

def adjust_angle(degree):
    """角度調整を行う関数"""
    if 170 < degree:
        degree -= 360
    if degree < -180:
        degree += 360
    return degree

def circle(r, cx, cy, orgx, orgy):
    for deg in range(0, 360):
        rad = deg / 360 * 2 * math.pi
        x = r * math.cos(rad)
        y = r * math.sin(rad)
        disp.pixel(int(cx + x + orgx), int(cy + y + orgy), 1)          
                     
def drow_nav(pitch, roll):
    disp.rect(0, 14, 128, 50, 1)
    disp.hline(0, 39, 128, 1)
    disp.vline(64, 14, 64, 1)
    cx = pitch / 180 *  64
    cy = roll / 180 * 25
    orgx = 64
    orgy = 39
    circle(6, cx, cy, orgx, orgy)

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)

i2c2 = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
disp = SSD1306_I2C(128, 64, i2c2)

while True:
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    zAccel = mpu.accel.z
    # print('x:', xAccel, 'y:', yAccel, 'z:', zAccel)

    if not(-0.0001 < zAccel < 0.0001):
        pitch = math.atan(yAccel / zAccel)
        roll = math.atan(xAccel / zAccel)
        pitchDeg = pitch / (2 * math.pi) * 360
        rollDeg = roll / (2 * math.pi) * 360
        if zAccel < 0:
            pitchDeg += 180
            rollDeg += 180
        pitchDeg = adjust_angle(pitchDeg)
        rollDeg = adjust_angle(rollDeg)
    
        disp.fill(0)
        message = "P:" + str(round(pitchDeg, 1)) + " R:" + str(round(rollDeg, 1))
        disp.text(message, 0, 0)
        drow_nav(pitchDeg, rollDeg)
        disp.show()
 
    utime.sleep(0.05)
