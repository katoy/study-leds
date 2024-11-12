from machine import Pin, PWM
from time import sleep

# 内蔵LEDはピン番号25に接続されています
led = PWM(Pin(25))   # LEDピンをPWMモードに設定
led.freq(1000)       # PWMの周波数を1kHzに設定

def set_brightness(percent):
    """
    LEDの明るさをパーセンテージで設定する関数
    :param percent: 0から100の範囲で指定する明るさ (％)
    """
    # 0から100%を0から65535の範囲にマッピング
    duty = int(65535 * (percent / 100))
    led.duty_u16(duty)

while True:
    # 明るさを0%から100%まで徐々に増加
    for i in range(0, 101, 5):  # 5%刻みで増加
        set_brightness(i)
        sleep(0.03)

    # 明るさを100%から0%まで徐々に減少
    for i in range(100, -1, -5):  # 5%刻みで減少
        set_brightness(i)
        sleep(0.03)
    sleep(0.5)

