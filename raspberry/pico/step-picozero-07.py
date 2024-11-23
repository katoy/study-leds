# 抵抗（330Ω または 1kΩ）
# 配線方法:
# GPIO 17 --- [アノード (+)]LED[カソード (-)] --- [抵抗 (330Ω)] --- GND
# GPIO 18 --- 同様の接続
# GPIO 19 --- 同様の接続

from picozero import LED
import time

# GPIO ピンに接続された LED
leds = [LED(17), LED(18), LED(19)]

# 各 LED の点灯時間 (秒)
times = [4, 2, 4]

# LED の点灯・消灯を管理する関数
def control_leds(leds, times):
    # 配列長チェック
    if len(leds) != len(times):
        raise ValueError("The length of 'leds' and 'times' must be the same.")

    for idx, led in enumerate(leds):
        led.on()                # LED を点灯
        time.sleep(times[idx])  # 対応する点灯時間だけ待機
        led.off()               # LED を消灯

try:
    # 各 LED を順番に点灯・消灯
    while True:
        control_leds(leds, times)

except KeyboardInterrupt:
    # Ctrl+C で終了時の処理
    print("\nExiting program. Turning off the LEDs.")
    for led in leds: # 全ての LED を消灯
        led.off()
    print("Program terminated.")
