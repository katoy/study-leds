from imu import MPU6050
from machine import I2C,Pin
import math
import utime
 
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
mpu = MPU6050(i2c)
 
# count = 10
# while count != 0:
#     xGyro = mpu.gyro.x
#     yGyro = mpu.gyro.y
#     zGyro = mpu.gyro.z
#     utime.sleep(0.05)
#     count -= 1

rollG = 0
pitchG = 0
rollComp = 0
pitchComp = 0
rollError = 0
pitchError = 0

yaw = 0
deltaTime = 0
count = 0

while True:
    tStart=utime.ticks_ms()
    
    xGyro = mpu.gyro.x
    yGyro = -mpu.gyro.y
    zGyro = mpu.gyro.z
    
    xAccel = mpu.accel.x
    yAccel = mpu.accel.y
    zAccel = mpu.accel.z
    
    rollG  += yGyro * deltaTime
    pitchG += xGyro * deltaTime
    
    rollA  = math.atan(xAccel / zAccel) / 2/ math.pi * 360 + rollError * 0.05
    pitchA = math.atan(yAccel / zAccel)/ 2 / math.pi * 360 + pitchError * 0.05
    
    rollComp= rollA * 0.005 + 0.995 * (rollComp + yGyro * deltaTime)
    pitchComp = pitchA * 0.005 + 0.995 * (pitchComp + xGyro * deltaTime)
    
    rollError += (rollA - rollComp) * deltaTime
    pitchError += (pitchA - pitchComp) * deltaTime
    
    count -= 1
    if count <= 0:
        count = 10
        print('RA: ',rollA,'PA: ',pitchA,'RC: ',rollComp,'PC: ',pitchComp)
    tStop = utime.ticks_ms()
    deltaTime = (tStop - tStart) * 0.001
