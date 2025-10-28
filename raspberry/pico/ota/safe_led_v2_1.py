"""
Safe LED Controller with Optional OTA
安全なLEDコントローラー（OTA機能は任意）
"""
import time
from machine import Pin

class SafeLEDController:
    """安全なLEDコントローラー"""

    def __init__(self, interval=0.2):
        self.led = Pin('LED', Pin.OUT)
        self.interval = interval
        self.running = False
        self.blink_count = 0

    def start(self):
        """LEDの点滅を開始"""
        print(f"LED点滅開始 (間隔: {self.interval}秒)")
        self.running = True

        try:
            while self.running:
                self.led.on()
                time.sleep(self.interval)
                self.led.off()
                time.sleep(self.interval)
                self.blink_count += 1

                # 10回点滅したら状況報告
                if self.blink_count % 10 == 0:
                    print(f"点滅回数: {self.blink_count}")

        except KeyboardInterrupt:
            print("中断されました")
        except Exception as e:
            print(f"エラー: {e}")
        finally:
            self.stop()

    def stop(self):
        """LEDの点滅を停止"""
        self.running = False
        self.led.off()
        print("LED停止")

def main():
    """メイン関数"""
    print("=== Safe LED Controller v2.1.0 ===")
    print("安全な基本LEDコントローラー")

    # 0.2秒間隔で点滅（v2.1.0の仕様）
    controller = SafeLEDController(interval=0.2)
    controller.start()

if __name__ == "__main__":
    main()