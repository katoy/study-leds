from machine import Pin, PWM
from time import sleep

led = PWM(Pin(17))   # LED ピンをPWMモードに設定
# led = PWM(Pin(25))   # for pico 内臓 LED
# led = PWM('LED')     # for pico w 内臓 led

led.freq(1000)       # PWM の周波数を 1kHz に設定

def set_brightness(percent):
    """
    LED の明るさをパーセンテージで設定する関数
    :param percent: 0 から 100 の範囲で指定する明るさ (％)
    """
    # 0 から m% を 0 から 65535 の範囲にマッピング
    duty = int(65535 * (percent / 100))
    led.duty_u16(duty)

while True:
    # 明るさを 0% から 100% まで徐々に増加
    for i in range(0, 101, 5):  # 5% 刻みで増加
        set_brightness(i)
        sleep(0.03)

    # 明るさを 100% から 0% まで徐々に減少
    for i in range(100, -1, -5):  # 5% 刻みで減少
        set_brightness(i)
        sleep(0.03)
    sleep(0.5)
