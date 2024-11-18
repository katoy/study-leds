# Raspberry Pi Pico の内蔵 LED を使用したメトロノームプログラム
#
# 機能概要:
# - Raspberry Pi Pico の内蔵 LED を一定のテンポで点滅させ、メトロノームとして視覚的にリズムを表示します。
# - BOOTSEL ボタンを使用してテンポ (BPM) を変更することが可能で、ボタンを押すごとに BPM が
#   10 増加します。
# - BPM が 180 を超えた場合、再び BPM を 60 にリセットしてテンポが遅くなります。
#
# 動作の詳細:
# 1. 初期 BPM を 60 に設定し、BPM に基づく 1 拍あたりの時間 (interval) を計算します。
# 2. メインループ内で内蔵 LED を点灯・消灯し、計算された interval に基づき次のビートまで待機します。
# 3. BOOTSEL ボタンが押されると BPM を 10 増加させ、 BPM に応じた interval を再計算します。
#    これにより、テンポが調整されます。
# 4. ボタンが押され続けた場合の誤動作を防ぐため、ボタン入力には 0.3 秒のデバウンス処理を加えています。
#
# 使用機能:
# - 内蔵 LED を使った視覚的なリズム表示(GPIO 25)
# - BOOTSEL ボタンによるテンポ調整機能
# - デバウンス処理で安定したボタン入力

import machine
import time
import bootsel

# BOOTSEL ボタンの状態を確認するためのメモリアドレス
BOOTSEL_BUTTON_ADDRESS = 0x40000054

def show_change_bmp(bpm):
    print(f"BPM: {bpm}")           # bpm を表示
    for _ in range(20):
        led.on()                   # LEDを点灯
        time.sleep(0.05)           # 0.1秒間点灯
        led.off()                  # LEDを消灯
        time.sleep(0.05)           # 0.1秒間消灯

# 初期設定
bpm = 60                           # 初期 BPM を 60 に設定
interval = 60 / bpm                # BPM から 1 拍あたりの間隔 (秒) を計算

# 内蔵 LED の設定(GPIO 25)
led = machine.Pin(25, machine.Pin.OUT)

print(f"BPM: {bpm}")               # bpm を表示
# メインループ: メトロノーム動作
while True:
    # BOOTSEL ボタンが押されたら BPM を調整
    if bootsel.pressed():
        bpm += 10                  # BPM を 10 増加
        if bpm > 180:
            bpm = 60               # 180 を超えたら BPM を 60 にリセット
        interval = 60 / bpm        # 更新された BPM で間隔を再計算
        time.sleep(0.3)            # デバウンス処理 (0.3 秒待機)
        show_change_bmp(bpm)

    # 内蔵 LED を使ってリズムを表示
    led.on()                       # LED 点灯 (ビートを示す)
    time.sleep(0.1)                # 0.1 秒間点灯
    led.off()                      # LED 消灯
    time.sleep(interval - 0.1)     # 次のビートまでの残りの間隔で待機
