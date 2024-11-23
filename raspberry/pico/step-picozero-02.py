# 配線方法
# GPIO 17 --- [抵抗] --- (+)LED1(-) --- GND
#
# 抵抗（330Ω または 1kΩ）

from picozero import LED
from picozero import pico_led
from time import sleep

# LED を設定
# led = pico_led
led = LED(17)  # GPIO 17 は外部接続の LED

try:
    while True:
        # 明るさを 0 から 1 まで徐々に増加
        for brightness in range(0, 101, 5):  # 5% 刻みで増加 (0～100)
            led.value = brightness / 100     # 0 ～ 1 の範囲で設定
            sleep(0.03)

        # 明るさを 1 から 0 まで徐々に減少
        for brightness in range(100, -1, -5):  # 5% 刻みで減少
            led.value = brightness / 100
            sleep(0.03)

        sleep(0.5)  # 循環ごとに少し待機

except KeyboardInterrupt:
    # Ctrl+C で終了時の処理
    print("\nExiting program. Turning off the LED.")
    led.off()  # LEDを消灯
    print("Program terminated.")
