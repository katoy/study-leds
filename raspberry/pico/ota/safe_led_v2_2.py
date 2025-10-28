"""
Safe LED Controller v2.2.0
安全なLEDコントローラー（1.0秒間隔）
"""
import time
from machine import Pin

class SafeLEDController:
    """安全なLEDコントローラー"""

    def __init__(self, interval=1.0):
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
                
                # 5回点滅したら状況報告
                if self.blink_count % 5 == 0:
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
    print("=== Safe LED Controller v2.2.0 ===")
    print("安全な基本LEDコントローラー（1.0秒間隔）")
    
    # 1.0秒間隔で点滅（v2.2.0の仕様）
    controller = SafeLEDController(interval=1.0)
    controller.start()

if __name__ == "__main__":
    main()