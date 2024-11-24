from picozero import PWMOutputDevice
from time import sleep, time  # 明示的に time をインポート

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

    def play_tone(self, duration, duty_cycle=0.5):
        """
        指定した時間とデューティ比でブザーを鳴らす。
        Args:
            duration (float): 音を鳴らす時間（秒）
            duty_cycle (float): PWMのデューティ比（0.0～1.0）
        """
        if not (0.0 <= duty_cycle <= 1.0):
            raise ValueError("duty_cycle must be between 0.0 and 1.0")

        self.buzzer.value = duty_cycle
        sleep(duration)
        self.buzzer.value = 0  # 明示的にブザーを停止

    def cuckoo_sound(self, total_duration, duty_cycle=0.5):
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


    def stop(self):
        """
        クラスの動作を停止します。
        """
        print("終了処理を開始します")
        
        # スレッドの停止フラグを設定
        self.button_thread_running = False
        
        # スレッドが停止するのを待機
        print("ボタン監視スレッドを停止中...")
        for _ in range(50):  # 最大 5 秒待機 (0.1 秒 × 50 回)
            time.sleep(0.1)
            if not self.button_thread_running:
                break
        else:
            print("警告: ボタン監視スレッドが正常に停止しませんでした")

        # 全てのLEDを消灯
        print("LED をすべて消灯します...")
        for led in self.leds.values():
            led.off()

        # ブザーを停止
        print("ブザーを停止します...")
        self.cuckoo.stop()

        print("終了処理が完了しました")

# メインプログラム
if __name__ == "__main__":
    cuckoo = CuckooSignal(gpio_pin=20)
    cuckoo.cuckoo_sound(total_duration=4)