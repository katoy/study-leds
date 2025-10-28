"""
メインアプリケーション v1.2.0 - シンプル版
- 0.2秒間隔での点滅
- 点滅カウンター機能
"""

from machine import Pin, Timer
import time
import gc

class SimpleLEDController:
    def __init__(self):
        self.led = Pin('LED', Pin.OUT)
        self.timer = Timer()
        self.interval = 200  # 0.2秒間隔
        self.running = False
        self.blink_count = 0

    def blink_callback(self, timer):
        """タイマーコールバック"""
        self.led.toggle()
        self.blink_count += 1
        print(f"LED: {self.led.value()} | Count: {self.blink_count}")

    def start(self):
        """点滅開始"""
        self.stop()
        self.timer.init(period=self.interval, mode=Timer.PERIODIC, callback=self.blink_callback)
        self.running = True
        print(f"Started blinking at {self.interval}ms interval")

    def stop(self):
        """点滅停止"""
        if self.running:
            self.timer.deinit()
            self.running = False
            self.led.off()
            print("LED stopped")

    def reset_counter(self):
        """点滅カウンターをリセット"""
        self.blink_count = 0
        print("Blink counter reset")

def main():
    print("=== Simple LED Controller v1.1.0 ===")
    print("Features: 0.5 second interval blinking, Blink counter")

    controller = SimpleLEDController()

    try:
        # 点滅開始
        print("\n--- Starting LED blink ---")
        controller.start()

        # メインループ
        while True:
            time.sleep(10)
            # 10秒ごとに点滅回数を表示
            print(f"Total blinks: {controller.blink_count}")
            gc.collect()

    except KeyboardInterrupt:
        print("\nApplication interrupted")
    finally:
        controller.stop()
        print("Application ended")

if __name__ == "__main__":
    main()