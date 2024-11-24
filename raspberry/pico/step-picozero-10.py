from picozero import LED, Button
from cuckoo_signal_active import CuckooSignal
import time
import _thread

class TrafficSignal:
    """
    信号機を制御するクラス。
    """
    def __init__(self, leds, cuckoo, button):
        """
        初期化メソッド。
        Args:
            leds (dict): 信号の各色に対応する LED インスタンスの辞書。
            cuckoo (CuckooSignal): カッコー音を制御するインスタンス。
            button (Button): ボタンのインスタンス。
        """
        self.leds = leds
        self.cuckoo = cuckoo
        self.button = button
        self.is_red_lit = True  # 初期状態では赤信号が点灯
        self.button_thread_running = True
        self.button_thread = None

        # ボタンを監視するスレッドを開始
        self.button_thread = _thread.start_new_thread(self._monitor_button, ())

    def _monitor_button(self):
        """
        ボタンを監視するスレッド。
        """
        print("ボタンが押されたか調べるスレッドが開始されました")
        while self.button_thread_running:
            if self.is_red_lit and self.button.is_pressed:
                print("ボタンが押されました。")
                self._button_pressed()
            time.sleep(0.1)  # 0.1秒ごとにボタンをチェック
        print("ボタン監視スレッドが終了しました")

    def _button_pressed(self):
        """
        ボタンが押された際の処理。
        """
        self.is_red_lit = False  # 赤信号を消灯するトリガー

        # ブザーを短く鳴らす
        print("ブザー: 鳴動")
        self.cuckoo.play_tone(duration=0.5)
        time.sleep(2)  # 2 秒待機
        self.leds["red"].off()

        # 信号パターンを実行
        self.run(signal_pattern)

        # パターン終了後に赤信号に戻る
        print("赤信号: 再点灯")
        self.is_red_lit = True
        self.leds["red"].on()

    def control_step(self, step):
        """
        信号機の単一ステップを制御します。
        Args:
            step (dict): 信号の単一ステップ定義。
        """
        led = self.leds[step["color"]]
        mode = step["mode"]

        if mode == "on":
            self._turn_on(led, step["duration"])
        elif mode == "on_with_cuckoo":
            self._turn_on_with_cuckoo(led, step["duration"])
        elif mode == "blink":
            self._blink(led, step["duration"], step["count"])
        else:
            raise ValueError(f"Unsupported mode: {mode}")

    def _turn_on(self, led, duration):
        """
        LED を点灯します。
        Args:
            led (LED): 点灯させる LED インスタンス。
            duration (float): 点灯時間（秒）。
        """
        print(f"{led} 点灯")
        led.on()
        time.sleep(duration)
        led.off()

    def _turn_on_with_cuckoo(self, led, duration):
        """
        LED を点灯しながらカッコー音を再生します。
        Args:
            led (LED): 点灯させる LED インスタンス。
            duration (float): 点灯およびカッコー音再生時間（秒）。
        """
        print(f"{led} 点灯 + カッコー音再生")
        led.on()
        self.cuckoo.cuckoo_sound(total_duration=duration)
        led.off()

    def _blink(self, led, duration, count):
        """
        LED を点滅させます。
        Args:
            led (LED): 点滅させる LED インスタンス。
            duration (float): 点滅間隔（秒）。
            count (int): 点滅回数。
        """
        print(f"{led} 点滅")
        for _ in range(count):
            led.on()
            time.sleep(duration)
            led.off()
            time.sleep(duration)

    def run(self, pattern):
        """
        信号機の全パターンを制御します。
        Args:
            pattern (list): 信号のパターン定義のリスト。
        """
        for step in pattern:
            self.control_step(step)

    def stop(self):
        """
        クラスの動作を停止します。
        """
        print("終了処理を開始します")
        self.button_thread_running = False
        time.sleep(0.2)  # スレッドの終了を待機
        for led in self.leds.values():
            led.off()
        self.cuckoo.stop()
        print("終了処理が完了しました")


# GPIO ピンに接続された LED、ブザー、ボタン
leds = {
    "red": LED(17),
    "yellow": LED(18),
    "blue": LED(19),
}
cuckoo = CuckooSignal(gpio_pin=20)
button = Button(16, pull_up=True)  # GPIO 16 に接続されたボタン

# 信号の点灯・点滅パターンの配列
signal_pattern = [
    {"color": "blue", "mode": "on_with_cuckoo", "duration": 4},  # 青 点灯 + カッコー音 4秒
    {"color": "blue", "mode": "blink", "duration": 0.5, "count": 4},  # 青 点滅 0.5秒を4回
    {"color": "yellow", "mode": "on", "duration": 2},  # 黄 点灯 2秒
]

# メインプログラム
if __name__ == "__main__":
    traffic_signal = TrafficSignal(leds, cuckoo, button)

    try:
        print("信号機シミュレーションを開始します。Ctrl+C で終了します。")
        # 赤信号を最初に点灯
        traffic_signal.leds["red"].on()
        while True:
            time.sleep(1)  # メインスレッドを維持
    except KeyboardInterrupt:
        print("\nプログラムを終了します。すべての LED を消灯します。")
        traffic_signal.stop()
        print("終了しました。")
