"""
メインアプリケーション v2.1.0 - OTA対応版
- 0.2秒間隔での点滅
- 点滅カウンター機能
- OTA自動更新機能
"""

import time
import gc
from machine import Pin, Timer
from lib.ota.ota_enabled_app import OTAEnabledApp

class SimpleLEDControllerOTA(OTAEnabledApp):
    def __init__(self):
        super().__init__(
            app_name="Simple LED Controller",
            version="2.1.0"
        )
        self.led = Pin('LED', Pin.OUT)
        self.timer = Timer()
        self.interval = 200  # 0.2秒間隔
        self.blink_count = 0
        self.led_running = False

    def blink_callback(self, timer):
        self.led.toggle()
        self.blink_count += 1
        print(f"LED: {self.led.value()} | Count: {self.blink_count}")

    def setup(self):
        print("\n--- Starting LED blink ---")
        self.timer.init(
            period=self.interval,
            mode=Timer.PERIODIC,
            callback=self.blink_callback
        )
        self.led_running = True
        print(f"Started blinking at {self.interval}ms interval")

    def loop(self):
        time.sleep(10)
        print(f"Total blinks: {self.blink_count}")
        gc.collect()

    def cleanup(self):
        if self.led_running:
            self.timer.deinit()
            self.led.off()
            print("LED stopped")

    def reset_counter(self):
        self.blink_count = 0
        print("Blink counter reset")

def main():
    app = SimpleLEDControllerOTA()
    app.run()

if __name__ == "__main__":
    main()
