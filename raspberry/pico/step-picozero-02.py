from picozero import LED
from time import sleep

# LEDピン (Picoでは内蔵LEDはピン番号25に接続されています)
led = LED(25)

def set_brightness(percent):
    """
    LEDの明るさをパーセンテージで設定する関数
    :param percent: 0から100の範囲で指定する明るさ (％)
    """
    # picozeroでは0から1の範囲で明るさを指定
    led.value = percent / 100

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
