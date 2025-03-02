"""
PIO-based LED Blink Example on Raspberry Pi Pico

概要:
  このスクリプトは、MicroPython と Raspberry Pi Pico の PIO (Programmable I/O) 機能を利用して、
  GPIO15 に接続された LED を 1 秒ごとに点灯・消灯させる例です。
  PIO アセンブリプログラムを用いて、LED の点灯・消灯と遅延処理を実現しています。

配線方法:
  図示の例
  【配線図】
  (Raspberry Pi Pico)
          +----------------+
          |                |
          |  GPIO15 (LED)  ---+---[330Ω]---|>|--- GND
          |                |
          +----------------+

動作環境:
  - Raspberry Pi Pico
  - MicroPython 実行環境
  - rp2 ライブラリを使用

作成者:
  [Your Name]

作成日:
  2025-03-02
"""

import rp2
from machine import Pin
import time

# PIO アセンブリプログラム
# sideset を使い、pinit の初期状態を LOW に設定しています。
# autopull=True で FIFO から 32bit（pull_thresh=32）ごとに OSR にロード
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32)
def blink():
    # LED ON フェーズ
    set(pins, 1)       .side(1)   # LED をオンに設定
    pull()                      # FIFO から 32bit の遅延カウントを受信
    mov(x, osr)                 # X レジスタに移す
    label("delay_on")
    set(y, 31)                  # 内側ループ用に Y レジスタに最大値 31 をセット
    label("inner_on")
    nop()                       # 1 サイクル待機
    jmp(y_dec, "inner_on")      # Y を 1 減算し、ゼロでなければ inner_on へジャンプ
    jmp(x_dec, "delay_on")      # 外側ループ：X を 1 減算し、ゼロでなければ delay_on へ

    # LED OFF フェーズ
    set(pins, 0)       .side(0)   # LED をオフに設定
    pull()                      # 次の遅延カウントを FIFO から受信
    mov(x, osr)
    label("delay_off")
    set(y, 31)
    label("inner_off")
    nop()
    jmp(y_dec, "inner_off")
    jmp(x_dec, "delay_off")
    wrap()                      # プログラムの先頭に戻る

# StateMachine を作成
# 周波数を 2MHz、sideset_base で GPIO15 を指定
sm = rp2.StateMachine(0, blink, freq=2000000, sideset_base=Pin(15))
sm.active(1)

# 遅延ループ用の外側ループの回数を計算
# 1 ループあたり約 33 サイクルなので、2,000,000/33 ≒ 60606 としています
DELAY_COUNT = 60606

# PIO 側は各フェーズで FIFO から値を必要とするので、継続的に供給します
while True:
    sm.put(DELAY_COUNT)  # LED ON 時の遅延値
    sm.put(DELAY_COUNT)  # LED OFF 時の遅延値
