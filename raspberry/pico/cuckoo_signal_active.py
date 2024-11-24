from picozero import PWMOutputDevice
from time import sleep, time

class CuckooSignal:
    """
    アクティブブザーを使って信号機のカッコー音を再現するクラス。
    """
    def __init__(self, gpio_pin):
        """
        初期化メソッド。
        Args:
            gpio_pin (int): 接続する GPIO ピン番号
        """
        self.buzzer = PWMOutputDevice(gpio_pin)
        self.stop_flag = False  # スレッド制御用のフラグ

    def play_tone(self, duration, duty_cycle):
        """
        指定した時間とデューティ比でブザーを鳴らす。
        Args:
            duration (float): 音を鳴らす時間（秒）
            duty_cycle (float): PWMのデューティ比（0.0～1.0）
        """
        if not (0.0 <= duty_cycle <= 1.0):
            raise ValueError("duty_cycle must be between 0.0 and 1.0")
        
        self.buzzer.value = duty_cycle  # デューティ比を設定
        sleep(duration)
        self.buzzer.off()

    def cuckoo_sound(self, total_duration=4, duty_cycle=0.5):
        """
        信号機のカッコー音を再現。
        Args:
            total_duration (float): 全体の再生時間（秒）
            duty_cycle (float): PWMのデューティ比（0.0～1.0）
        """
        end_time = time() + total_duration
        while time() < end_time:
            # ミ
            self.play_tone(0.5, duty_cycle)
            sleep(0.1)  # 短い間隔
            # ソ
            self.play_tone(0.5, duty_cycle)
            sleep(0.3)  # 長い間隔

    def run(self, duty_cycle):
        """
        カッコー音を繰り返し再生。
        stop_flag が True になるまで続ける。
        Args:
            duty_cycle (float): PWMのデューティ比（0.0～1.0）
        """
        while not self.stop_flag:
            self.cuckoo_sound(duty_cycle)

    def stop(self):
        """
        ブザーを停止し、ループを終了。
        """
        self.stop_flag = True
        self.buzzer.off()


# メインプログラム
if __name__ == "__main__":
    cuckoo = CuckooSignal(gpio_pin=20)
    cuckoo.cuckoo_sound(duty_cycle=0.5)  # デューティ比 0.5 で再生

