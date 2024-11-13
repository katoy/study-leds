from machine import Pin, PWM
import time
import math
import urandom as random  # MicroPython では random の代わりに urandom を使う

# LED の接続ピンの設定
LED_PIN = 17  # Pico の GPIO ピン番号 (例: GPIO17)
led = PWM(Pin(LED_PIN))
led.freq(1000)  # 1000 Hz で PWM 制御

# 炎の揺らぎパターンを関数として定義
def sine_random_flame_pattern():
    """サイン波とランダムノイズを組み合わせた揺らぎパターン"""
    t = 0
    while True:
        base_brightness = 50 + 50 * math.sin(t)
        noise = random.getrandbits(4) - 8  # -8 から 7 までのランダムノイズ
        yield max(0, min(100, int(base_brightness + noise)))
        t += 0.1

def random_walk_flame_pattern():
    """ランダムウォークによる揺らぎパターン"""
    brightness = 75
    while True:
        change = random.getrandbits(4) - 8  # -8 から 7 までのランダム変化
        brightness = max(50, min(100, brightness + change))
        yield brightness
        time.sleep(0.1)

def multi_sine_flame_pattern():
    """複数のサイン波を組み合わせた揺らぎパターン"""
    t = 0
    while True:
        brightness = 50 + 20 * math.sin(t) + 15 * math.sin(0.5 * t) + (random.getrandbits(4) - 8)
        yield max(0, min(100, int(brightness)))
        t += 0.1

# パターンの選択（MicroPython では直接関数を選択）
# flame_pattern = sine_random_flame_pattern
# flame_pattern = random_walk_flame_pattern
flame_pattern = multi_sine_flame_pattern

try:
    # 選択したパターンでLEDの明るさを制御
    for brightness in flame_pattern():
        # PWMのDutyサイクルを調整（0-65535の範囲に変換）
        led.duty_u16(int(brightness * 655.35))  # 100を65535に対応させる
        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    led.deinit()

