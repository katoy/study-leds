# 配線方法
# [GPIO 16] --- [ボタン] --- [GND]

"""
クリック判定プログラム

このプログラムは、Raspberry Pi Pico に接続されたボタン (GPIO16) を使用して、
以下の 3 種類のクリックタイプを判定し、結果を出力します。

1. Single Click (シングルクリック)
   - ボタンを 1 回短く押すと判定されます。
2. Double Click (ダブルクリック)
   - ボタンを短い間隔で 2 回押すと判定されます。
3. Long Press (長押し)
   - ボタンを 1 秒以上押し続けると判定されます。

機能:
- ボタンの押下と解放をイベントとして処理します (ポーリング不要)。
- 判定されたクリックタイプを 1 回だけ出力します。

使用方法:
- プログラムを Raspberry Pi Pico 上で実行してください。
- GPIO16 ピンにボタンを接続し、片方を GND に接続します。

注意:
- クリック間隔 (CLICK_INTERVAL) や長押し判定時間 (LONG_PRESS_DURATION) は、
  必要に応じて調整可能です。
"""

from picozero import Button
from time import time, sleep

# 定数設定
LONG_PRESS_DURATION = 1  # 長押しの判定時間 (秒)
CLICK_INTERVAL = 0.4     # クリック間の最大間隔 (秒)
POLL_INTERVAL = 0.1      # 判定ポーリング間隔 (秒)

button = Button(16, pull_up=True)  # 内部プルアップ抵抗を有効化

# 状態管理変数
click_count = 0
press_start_time = 0
last_release_time = 0
is_long_press = False
click_result = None  # 判定結果を格納


def record_press_time():
    """ボタンが押された時刻を記録"""
    global press_start_time, is_long_press
    press_start_time = time()
    is_long_press = False  # 長押しフラグをリセット


def handle_release():
    """ボタンが離された時の処理"""
    global click_count, is_long_press, last_release_time, click_result

    release_time = time()
    press_duration = release_time - press_start_time

    if press_duration >= LONG_PRESS_DURATION:
        click_result = "Long Press"
        is_long_press = True
        click_count = 0  # 長押しの場合、クリックカウントをリセット
    else:
        click_count += 1
        last_release_time = release_time  # 最後のクリック時間を更新


def determine_click_type():
    """クリックタイプを判定して結果を更新"""
    global click_count, last_release_time, is_long_press, click_result

    current_time = time()
    if click_count > 0 and (current_time - last_release_time > CLICK_INTERVAL) and not is_long_press:
        if click_count == 1:
            click_result = "Single Click"
        elif click_count == 2:
            click_result = "Double Click"
        click_count = 0  # 判定後にリセット


def print_click_result():
    """クリック結果を出力"""
    global click_result
    if click_result:
        print(click_result)
        click_result = None  # 出力後にリセット


# 割り込みの設定
button.when_pressed = record_press_time
button.when_released = handle_release

# メインループでクリックタイプを管理
while True:
    determine_click_type()  # クリックタイプを判定
    print_click_result()    # 判定結果を出力
    sleep(POLL_INTERVAL)
