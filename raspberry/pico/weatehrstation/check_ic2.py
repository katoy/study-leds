from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# I2Cの初期化
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=50000)

# I2Cアドレスを確認
devices = i2c.scan()
print(f"I2Cデバイス: {devices}")
if 0x3C not in devices:
    print("SSD1306デバイスが見つかりません。")
else:
    print("SSD1306デバイスを検出しました (アドレス: 0x3C)")

try:
    addr = 0x3C  # OLEDディスプレイのアドレス
    # cmd = bytearray([0xAE])  # ディスプレイOFFコマンド
    cmd = bytearray([0xAF])  # ディスプレイONコマンド
    time.sleep(1)  # 初期化時間を確保
    i2c.writeto(addr, cmd)  # コマンド送信
    print("コマンド送信成功。I2C通信は正常です。")
except OSError as e:
    print(f"I2C通信に失敗しました: {e}")
