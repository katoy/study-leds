# 配線
# [GPIO 17 (物理ピン 11)] --- (+)LED(-) --- [330Ω 抵抗] --- [GND (物理ピン 6)]
#

from gpiozero import LED
from time import sleep

# GPIO 17 ピンを制御する LED オブジェクトを作成
led = LED(17)

try:
    while True:
        led.on()         # LED を ON
        print("LED ON")
        sleep(1)         # 1 秒間待機

        led.off()        # LED を OFF
        print("LED OFF")
        sleep(1)         # 1 秒間待機

except KeyboardInterrupt:
    # Ctrl + C が押された時に実行
    print("終了します")
    led.off()           # LED を OFF にして終了

