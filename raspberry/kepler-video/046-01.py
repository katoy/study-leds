from imu import MPU6050
from machine import I2C, Pin
import utime


i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)
          
while True:
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    zAccel = mpu.accel.z
    print('x:', xAccel, 'y:', yAccel, 'z:', zAccel)
    
    utime.sleep(0.1)
