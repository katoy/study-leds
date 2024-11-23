# 配線
# GPIO 20 --- [アノード (+)]ブザー[カソード (-)] --- GND
#

from picozero import PWMOutputDevice
from time import sleep

from picozero import Buzzer
import time  # 必要な time モジュールをインポート

# GPIO 20 に接続されたブザーを制御
buzzer = Buzzer(20)

try:
    while True:
        print("Buzzer ON")  # ブザーが ON になったことを表示
        buzzer.on()         # ブザーを ON
        time.sleep(1)       # 1 秒間鳴らす

        print("Buzzer OFF") # ブザーが OFF になったことを表示
        buzzer.off()        # ブザーを OFF
        time.sleep(0.5)     # 0.5 秒間待機
except KeyboardInterrupt:
    # プログラム終了時の処理
    print("\nProgram terminated by user. Turning off the buzzer.")
    buzzer.off()  # ブザーを停止
