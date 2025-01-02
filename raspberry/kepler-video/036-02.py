from picozero import Servo
import utime

# サーボピンを指定
servoPin = 15

# サーボモーターの初期化
servo = Servo(servoPin)

# -0.5: 0 度, 0: 45 度, 0.5: 90 度, 1.5: 180 度
servo.value = -0.5
utime.sleep(2)

while True:
    angle = int(input('What angle do you desire? '))
    if 0 <= angle <= 180:
        servo.value = (angle - 45) / 90.0  # 指定した角度にサーボを動かす
        utime.sleep(0.5)
    else:
        print("Please enter a value between 0 and 180.")
