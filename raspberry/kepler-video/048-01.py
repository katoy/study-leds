from imu import MPU6050
from machine import I2C, Pin
import utime


i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)
utime.sleep(0.5)

roll = pitch = you = 0

count = 10
while count != 0:
    xGyro = mpu.gyro.x
    yGyro = mpu.gyro.y
    zGyro = mpu.gyro.z
    utime.sleep(0.05)
    count -= 1

utime.sleep(0.5)
count = 0
while True:
    startTime = utime.ticks_ms()
    xGyro = mpu.gyro.x
    yGyro = mpu.gyro.y
    zGyro = mpu.gyro.z    
    utime.sleep(0.02)
    stopTime = utime.ticks_ms()
    deltaTime = (stopTime - startTime) / 1000.0

    roll  += deltaTime * xGyro
    pitch += deltaTime * yGyro
    you   += deltaTime * zGyro
    
    count -= 1
    if count <= 0:
        # print('r:', xGyro, 'p:', yGyro, 'y:', zGyro)
        print('r:', roll, 'p:', pitch, 'y:', you)
        count = 10
