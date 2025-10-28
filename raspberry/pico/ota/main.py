import time
from machine import Pin
led = Pin('LED', Pin.OUT)
blink_count = 0
for i in range(10):
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
    led.toggle()
    blink_count += 1
    print(f"LED: {led.value()} | Count: {blink_count}")

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
    print("=== Simple LED Controller v1.2.0 ===")
    print("Features: 1 second interval blinking, Blink counter")

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
