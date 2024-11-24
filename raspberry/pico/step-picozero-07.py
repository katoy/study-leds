# 抵抗（330Ω または 1kΩ）
# 配線方法:
# GPIO 17 --- [アノード (+)]LED[カソード (-)] --- [抵抗 (330Ω)] --- GND
# GPIO 18 --- 同様の接続
# GPIO 19 --- 同様の接続

from picozero import LED
from cuckoo_signal_active import CuckooSignal
import time


class TrafficSignal:
    """
    信号機を制御するクラス。
    """
    def __init__(self, leds, cuckoo):
        """
        初期化メソッド。
        Args:
            leds (dict): 信号の各色に対応する LED インスタンスの辞書。
            cuckoo (CuckooSignal): カッコー音を制御するインスタンス。
        """
        self.leds = leds
        self.cuckoo = cuckoo

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

# GPIO ピンに接続された LED とブザー
leds = {
    "red": LED(17),
    "yellow": LED(18),
    "blue": LED(19),
}
cuckoo = CuckooSignal(gpio_pin=20)

# 信号の点灯・点滅パターンの配列
signal_pattern = [
    {"color": "red", "mode": "on", "duration": 4},  # 赤 点灯 4秒
    {"color": "blue", "mode": "on_with_cuckoo", "duration": 4},  # 青 点灯 + カッコー音 4秒
    {"color": "blue", "mode": "blink", "duration": 0.5, "count": 4},  # 青 点滅 0.5秒を4回
    {"color": "yellow", "mode": "on", "duration": 2},  # 黄 点灯 2秒
]

# メインプログラム
traffic_signal = TrafficSignal(leds, cuckoo)

try:
    print("信号機シミュレーションを開始します。Ctrl+C で終了します。")
    while True:
        traffic_signal.run(signal_pattern)
except KeyboardInterrupt:
    print("\nプログラムを終了します。すべての LED を消灯します。")
    for led in leds.values():
        led.off()
    cuckoo.stop()
    print("終了しました。")
