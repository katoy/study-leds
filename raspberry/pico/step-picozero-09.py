# 配線
# GPIO 20 --- [アノード (+)]ブザー[カソード (-)] --- GND
#

from picozero import PWMOutputDevice
from time import sleep

# GPIO 20 に接続されたブザーを制御 (PWMOutputDevice を使用)
buzzer = PWMOutputDevice(20)

def set_volume(volume):
    """
    ブザーの音量を設定する関数
    :param volume: 0（無音）～100（最大音量）の範囲で指定
    """
    buzzer.value = volume / 100  # デューティ比を 0.0 ～ 1.0 に設定

try:
    while True:
        # 音量を徐々に増加
        for volume in range(0, 101, 10):  # 0% から 100% まで 10% 刻みで増加
            set_volume(volume)
            print(f"Volume: {volume}%")
            sleep(0.2)

        # 音量を徐々に減少
        for volume in range(100, -1, -10):  # 100% から 0% まで 10% 刻みで減少
            set_volume(volume)
            print(f"Volume: {volume}%")
            sleep(0.2)

except KeyboardInterrupt:
    print("\nProgram terminated by user. Turning off the buzzer.")
    buzzer.off()  # プログラム終了時にブザーを停止
