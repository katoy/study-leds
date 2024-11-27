"""
Raspberry Pi Pico の内部温度センサーを使用して CPU 温度を取得し、指定間隔でテキストファイルに記録するプログラム。

機能:
1. 内部温度センサーを使用して CPU 温度を取得。
2. サンプリング間隔（秒）と記録時間（秒）を指定可能。
3. 温度データをリアルタイムでコンソールに表示。
4. 取得した温度データを CSV形式で指定ファイルに保存。
5. 記録中に `Ctrl+C` を押すと記録を安全に停止。
"""

from picozero import pico_temp_sensor
from time import sleep, time


class CPULogger:
    """
    CPU 温度を取得してファイルに記録するクラス。
    """

    def __init__(self, interval=1, duration=60, filename="cpu_temperature_log.txt"):
        """
        初期化メソッド。
        Args:
            interval (float): サンプリング間隔（秒）。
            duration (float): 総記録時間（秒）。
            filename (str): ログファイルの名前。
        """
        self.sensor = pico_temp_sensor  # 既存の pico_temp_sensor を利用
        self.interval = interval
        self.duration = duration
        self.filename = filename
        self.running = False

    def start_logging(self):
        """
        CPU 温度を取得してログを記録するメソッド。
        """
        self.running = True
        start_time = time()

        try:
            with open(self.filename, "w") as file:
                file.write("Time (s), Temperature (C)\n")  # CSV ヘッダー
                while self.running and time() - start_time < self.duration:
                    elapsed_time = time() - start_time
                    temperature = self.sensor.temp  # 温度センサーの値を取得
                    self._log_to_file(file, elapsed_time, temperature)
                    self._log_to_console(elapsed_time, temperature)
                    sleep(self.interval)
        except Exception as e:
            print(f"エラーが発生しました: {e}")
        finally:
            print(f"記録を終了しました。ログは '{self.filename}' に保存されました。")

    def stop_logging(self):
        """
        ログ記録を安全に停止するメソッド。
        """
        self.running = False
        print("記録を停止中です...")

    @staticmethod
    def _log_to_file(file, elapsed_time, temperature):
        """
        温度データをファイルに書き込む。
        Args:
            file (file object): 書き込み対象のファイルオブジェクト。
            elapsed_time (float): 経過時間（秒）。
            temperature (float): CPU 温度（摂氏）。
        """
        file.write(f"{elapsed_time:.2f}, {temperature:.2f}\n")

    @staticmethod
    def _log_to_console(elapsed_time, temperature):
        """
        温度データをコンソールに表示する。
        Args:
            elapsed_time (float): 経過時間（秒）。
            temperature (float): CPU 温度（摂氏）。
        """
        print(f"Time: {elapsed_time:.2f}s, Temperature: {temperature:.2f}C")


# 設定
INTERVAL = 2  # サンプリング間隔（秒）
DURATION = 60  # 総記録時間（秒）

if __name__ == "__main__":
    logger = CPULogger(interval=INTERVAL, duration=DURATION)

    try:
        print("CPU 温度の記録を開始します。Ctrl+C で終了します。")
        logger.start_logging()
    except KeyboardInterrupt:
        print("\nCtrl+C により記録を中断しました。")
        logger.stop_logging()
    finally:
        print("プログラムを終了します。")
