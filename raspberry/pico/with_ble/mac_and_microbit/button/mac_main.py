#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import threading
from kaspersmicrobit import KaspersMicrobit

# ─── グローバル変数 ─────────────────────────────────
# B ボタン押下をメインループに通知するイベント
stop_event = threading.Event()

# ─── コールバック定義 ────────────────────────────────
def on_press_a(button):
    """A ボタン押下時の処理"""
    print(f"[A] Button {button} pressed")


def on_press_b(button):
    """B ボタン押下時の処理：メインスレッドに停止シグナルを送る"""
    print(f"[B] Button {button} pressed → signaling stop")
    stop_event.set()


# ─── メイン処理 ──────────────────────────────────────
def main():
    # 最初に見つかった micro:bit を with ブロックで接続／切断管理
    with KaspersMicrobit.find_one_microbit() as mb:
        # ボタン A 押下時コールバックを登録
        mb.buttons.on_button_a(
            press=on_press_a,
            long_press=None,
            release=None
        )

        # ボタン B 押下時コールバックを登録
        mb.buttons.on_button_b(
            press=on_press_b,
            long_press=None,
            release=None
        )

        # メインループ：stop_event がセットされるまで待機
        print("Waiting for B button press to exit...")
        while not stop_event.is_set():
            time.sleep(0.1)

    # with ブロックを抜けると自動で切断されるので、ここで正常終了
    print("Disconnected. Exiting program.")
    sys.exit(0)


if __name__ == "__main__":
    main()
