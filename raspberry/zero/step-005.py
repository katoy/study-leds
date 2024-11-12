"""
LED Flame Simulation Program
----------------------------
このプログラムは、Raspberry Pi の GPIO ピンを使用して LED の明るさを調整し、炎のような自然な揺らぎを再現します。
複数の揺らぎアルゴリズム（パターン）を選択可能で、実行時のパラメータでパターンを指定することができます。

使い方:
    このプログラムを実行する際に、`--pattern` 引数で使用するパターンを指定してください。
    各パターンは、LED の明るさの変化に異なるアルゴリズムを使用して、炎の揺らぎを表現します。
    
    例:
        python flame_led.py --pattern perlin        # パーリンノイズによる揺らぎ
        python flame_led.py --pattern sine_random   # サイン波 + ランダムノイズの揺らぎ
        python flame_led.py --pattern random_walk   # ランダムウォークによる揺らぎ
        python flame_led.py --pattern multi_sine    # 複数サイン波の揺らぎ

引数:
    --pattern : 使用する炎のパターンを指定します。以下のいずれかを選択してください。
                - 'perlin'       : パーリンノイズによる揺らぎ
                - 'sine_random'  : サイン波とランダムノイズの組み合わせによる揺らぎ
                - 'random_walk'  : ランダムウォークによる揺らぎ
                - 'multi_sine'   : 複数のサイン波の重ね合わせによる揺らぎ

アルゴリズムの概要:
    1. パーリンノイズ ('perlin')
       - 自然で滑らかなノイズを生成するパーリンノイズを使用して、ランダム性の中に規則性を持った明るさの揺らぎを再現します。
       - ベースとなる位置を少しずつ変化させることで、炎のゆらめきに似た動きを生み出します。
    
    2. サイン波＋ランダムノイズ ('sine_random')
       - サイン波の周期的な変化にランダムノイズを加えることで、自然な揺らぎを表現します。
       - サイン波による規則的な上下動が基礎となり、ランダムノイズが不規則性を加えるため、炎のリアルな動きを再現します。
    
    3. ランダムウォーク ('random_walk')
       - 前回の明るさにランダムに増減を加える「ランダムウォーク」を使い、炎の不規則なゆらめきを表現します。
       - 直前の明るさから大きく逸脱しないようにして、自然な変化が続くようにしています。
    
    4. 複数サイン波の重ね合わせ ('multi_sine')
       - 異なる周波数と振幅のサイン波を複数重ね合わせて、複雑で有機的な揺らぎを再現します。
       - 追加のランダムノイズを含むことで、豊かな変化がありながらも自然な炎の効果が得られます。

ハードウェア要件:
    - Raspberry Pi
    - LED （1つ以上のLEDで動作しますが、赤やオレンジの LED が炎の再現に適しています）
    - GPIO ピンへの適切な抵抗（330Ωなど）

コードの構成:
    - argparse : 起動時のパラメータ解析に使用
    - noise    : パーリンノイズの生成に使用（pip install noiseでインストール可能）
    - 各パターン関数 : 指定されたパターンに基づき、異なる揺らぎを生成するジェネレータ関数
    - メインループ : 選択されたパターンで生成される明るさをPWM制御に反映し、LEDを揺らぎのある炎のように点灯させます。

"""
import RPi.GPIO as GPIO
import time
import math
import random
import argparse
import noise  # Perlin noiseライブラリ (pip install noise)

# GPIO ピンの設定
LED_PIN = 17  # LED が接続されている GPIO ピン
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# PWM 設定
pwm = GPIO.PWM(LED_PIN, 100)  # 100 Hz で PWM を初期化
pwm.start(0)

# 引数の解析
parser = argparse.ArgumentParser(description="炎の揺らぎパターンを指定します")
parser.add_argument('--pattern', choices=['perlin', 'sine_random', 'random_walk', 'multi_sine'], 
                    default='sine_random', help="炎の揺らぎパターンを選択します")
args = parser.parse_args()


def perlin_flame_pattern():
    """パーリンノイズを使った揺らぎパターン"""
    base = random.random() * 100
    while True:
        # Perlinノイズの値 [-1.0 から 1.0] を [0.0 から 1.0] に正規化
        noise_value = (noise.pnoise1(base, repeat=1024) + 1) / 2
        brightness = noise_value * 100  # 0.0 から 100.0 の範囲にスケーリング
        brightness = max(0, min(100, brightness))  # 範囲外の値をクリップ
        yield brightness
        base += 0.05

def sine_random_flame_pattern():
    """サイン波とランダムノイズを組み合わせた揺らぎパターン"""
    t = 0
    while True:
        base_brightness = 50 + 50 * math.sin(t)
        noise = random.uniform(-15, 15)
        yield max(0, min(100, int(base_brightness + noise)))
        t += 0.1

def random_walk_flame_pattern():
    """ランダムウォークによる揺らぎパターン"""
    brightness = 75
    while True:
        change = random.uniform(-10, 10)
        brightness = max(50, min(100, brightness + change))
        yield int(brightness)
        time.sleep(0.1)

def multi_sine_flame_pattern():
    """複数のサイン波を組み合わせた揺らぎパターン"""
    t = 0
    while True:
        brightness = 50 + 20 * math.sin(t) + 15 * math.sin(0.5 * t) + random.uniform(-5, 5)
        yield max(0, min(100, int(brightness)))
        t += 0.1

# 選択されたパターンに対応するジェネレータを選ぶ
if args.pattern == 'perlin':
    flame_pattern = perlin_flame_pattern
elif args.pattern == 'sine_random':
    flame_pattern = sine_random_flame_pattern
elif args.pattern == 'random_walk':
    flame_pattern = random_walk_flame_pattern
elif args.pattern == 'multi_sine':
    flame_pattern = multi_sine_flame_pattern

try:
    # 選択したパターンで LED を制御
    for brightness in flame_pattern():
        pwm.ChangeDutyCycle(brightness)
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

finally:
    pwm.stop()
    GPIO.cleanup()

