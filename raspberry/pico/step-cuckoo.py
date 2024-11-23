from picozero import PWMOutputDevice
from time import sleep
import _thread
from cuckoo_signal_active import CuckooSignal

def start_cuckoo(duty_cycle):
    """
    カッコー音再生スレッドを開始。
    Args:
        duty_cycle (float): PWMのデューティ比（0.0～1.0）
    """
    cuckoo.stop_flag = False  # フラグをリセット
    _thread.start_new_thread(cuckoo.run, (duty_cycle,))

cuckoo = CuckooSignal(gpio_pin=20)
try:
    print("カッコー音を再生します。Ctrl+C で停止します。")

    # 音量を変化させる
    print("音量を0.1に設定")
    start_cuckoo(0.1)
    sleep(5)  # 5秒間再生

    print("音量を0.3に設定")
    cuckoo.stop()  # 前のスレッドを停止
    sleep(1)  # スレッドの切り替えのために1秒待機
    start_cuckoo(0.3)
    sleep(5)

    print("音量を0.6に設定")
    cuckoo.stop()
    sleep(1)
    start_cuckoo(0.6)
    sleep(5)

except KeyboardInterrupt:
    print("\n終了します。")
    cuckoo.stop()
