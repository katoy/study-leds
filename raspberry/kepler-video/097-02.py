"""
Raspberry Pi Pico - PIO を使用したサーボモータ制御

【概要】
- PIO (Programmable I/O) を使用して、GPIO20 に PWM 信号を生成し、サーボモータを制御する。
- PWM 周波数は 50Hz (周期 20ms) に設定。
- 角度 0° ～ 180° に対応する PWM パルス幅を計算し、サーボを駆動する。
- PIO の `freq=2_000_000` (2 MHz) に設定することで、0.5µs 単位の高精度な制御を実現。

【配線図】
```
      (Raspberry Pi Pico)
        +----------------+
        |                |
        |  GPIO20 (Servo) ---+---[Servo Signal]
        |                |
        +----------------+
```

【使用部品】
- Raspberry Pi Pico
- サーボモータ (SG90 など)
- 電源 (3.3V または 5V, 外部電源推奨)

【接続】
- サーボモータのVCC → Picoの5V (または外部電源)
- サーボモータのGND → PicoのGND
- サーボモータのSignal → PicoのGPIO20

【動作】
- PIO を使用して 50Hz の PWM 信号を生成。
- 角度 0° に対応する PWM 信号 (500µs) を初期値として設定。
- 角度を変更する際に `set_servo_angle(angle)` を呼び出すことで PWM パルス幅を変更。
- 0° から 180° まで 30° 刻みで変更し、その後 180° から 0° に戻るデモを実行。
- `Ctrl+C` でプログラムを終了すると PIO を停止し、サーボを 0° に戻す。

【注意】
- サーボモータの電源が不足すると動作が不安定になるため、外部電源を使用することを推奨。
- PIO を使用することで、CPU の負荷を抑えつつ正確な PWM 信号を生成可能。
- PIO の `freq=2_000_000` (2 MHz) に設定することで、1 クロック = 0.5µs の高精度制御が可能。
- `freq=1_000_000` (1 MHz) では 1 µs 単位でしか制御できず、PWM の精度が低下するため、推奨しない。
"""

import utime
from machine import Pin
import rp2

# PIO プログラム：サーボ用 PWM 信号を生成
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def servo_pio():
    label("main_loop")  # メインループの開始
    pull()              # ホストから HIGH のパルス幅を取得
    mov(y, osr)         # HIGH の時間を Y レジスタに保存
    set(pins, 1)        # PWM HIGH 開始
    label("high_loop")
    jmp(y_dec, "high_loop") [1]  # HIGH を維持
    set(pins, 0)        # PWM LOW 開始
    pull()              # ホストから LOW の時間を取得
    mov(x, osr)         # LOW の時間を X レジスタに保存
    label("low_loop")
    jmp(x_dec, "low_loop") [1]  # LOW を維持
    jmp("main_loop")    # 次の信号を待つ

# PIO ステートマシンの設定
sm = rp2.StateMachine(0, servo_pio, freq=2_000_000, set_base=Pin(20))
sm.active(1)

def set_servo_angle(angle):
    """指定した角度に応じた PWM パルス幅を PIO に送信"""
    high_time = int((angle / 180) * 2000 + 500)  # 角度に対する正確なパルス幅計算
    low_time = 20000 - high_time  # LOW の時間を Python 側で計算
    sm.put(high_time)  # HIGH の時間を PIO に送信
    sm.put(low_time)   # LOW の時間を PIO に送信
    print(f"Set angle: {angle}, Pulse width: {high_time} µs, Low time: {low_time} µs")

# 初期設定：0度
set_servo_angle(0)

# サーボを動かすデモ
try:
    while True:
        for angle in range(0, 181, 30):  # 0° から 180° まで 30° 刻みで変更
            set_servo_angle(angle)
            utime.sleep(1)
        for angle in range(180, -1, -30):  # 180° から 0° まで戻る
            set_servo_angle(angle)
            utime.sleep(1)
except KeyboardInterrupt:
    print("プログラム終了")
    set_servo_angle(0)  # サーボを 0° に戻す
    sm.active(0)  # PIO を停止
