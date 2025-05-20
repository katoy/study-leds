#!/usr/bin/env python3
import asyncio
import sys
from pynput import keyboard  # pynput ライブラリをインポート
from bleak import BleakScanner, BleakClient
from threading import Thread

# ————————————————————————————————
# デバイス／サービス／キャラクタリスティック UUID
# ————————————————————————————————
TARGET_NAME            = "BBC micro:bit"
BUTTON_SERVICE_UUID    = "e95d9882-251d-470a-a062-fa1922dfa9a8"
BUTTON_A_UUID          = "e95dda90-251d-470a-a062-fa1922dfa9a8"
BUTTON_B_UUID          = "e95dda91-251d-470a-a062-fa1922dfa9a8"

UART_SERVICE_UUID      = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID      = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # write (PC→micro:bit)
UART_TX_CHAR_UUID      = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # notify (micro:bit→PC)

# 非同期でボタンAが押されたときの処理
async def on_button_a(sender, data):
    print("▶ Button A pressed")

# 非同期でボタンBが押されたときの処理
async def on_button_b(sender, data):
    print("▶ Button B pressed - Exiting...")
    loop = asyncio.get_event_loop()  # 現在のイベントループを取得
    loop.stop()  # イベントループを停止してプログラムを終了する

# UARTデータを受け取った時の処理
async def handle_uart_rx(sender: int, data: bytearray):
    try:
        text = data.decode().strip()
        print(f"⟶ Received UART: {text}")
    except UnicodeDecodeError:
        print(f"⟶ Received raw UART: {data}")

# 非同期でユーザーコマンドを受け取る
async def read_commands(client):
    # グローバルフラグを設定
    keys_pressed = set()

    # キーボードの入力イベントを処理する関数
    def on_press(key):
        try:
            if hasattr(key, 'char') and key.char:  # key.char がある場合のみ処理
                if key.char == '1':
                    keys_pressed.add('1')
                elif key.char == '2':
                    keys_pressed.add('2')
                elif key.char == 'q':
                    keys_pressed.add('q')
        except AttributeError:
            # 特殊キーは無視
            pass

    def on_release(key):
        try:
            if hasattr(key, 'char') and key.char:  # key.char がある場合のみ処理
                if key.char == '1':
                    keys_pressed.remove('1')
                elif key.char == '2':
                    keys_pressed.remove('2')
                elif key.char == 'q':
                    keys_pressed.remove('q')
            if key == keyboard.Key.esc:
                return False  # ESCキーで終了
        except AttributeError:
            pass

    # キーボードリスナーを非同期に実行
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()  # 非同期でリスニングを開始

    # 非同期でコマンドを処理
    while True:
        if '1' in keys_pressed:
            await client.write_gatt_char(UART_RX_CHAR_UUID, b"on\n")
            print("✔ Sent UART: on")
        elif '2' in keys_pressed:
            await client.write_gatt_char(UART_RX_CHAR_UUID, b"off\n")
            print("✔ Sent UART: off")
        elif 'q' in keys_pressed:
            print("Exiting...")
            break

        await asyncio.sleep(0.1)  # 処理を軽くするために待機

# メイン処理
async def main():
    # 1) デバイス探索: 名前フィルタ or ボタンサービス UUID フィルタ
    print("Scanning for micro:bit...")
    device = await BleakScanner.find_device_by_filter(
        lambda d, adv: (
            adv.local_name and TARGET_NAME in adv.local_name
        ) or (
            BUTTON_SERVICE_UUID in adv.service_uuids
        ),
        timeout=10.0
    )

    if not device:
        print("micro:bit が見つかりませんでした")
        return

    # 2) BLE 接続
    async with BleakClient(device) as client:
        if not client.is_connected:
            print("接続に失敗しました")
            return
        print(f"Connected: {device.address}")

        # 4) ボタン A/B 通知ハンドラ
        await client.start_notify(
            BUTTON_A_UUID,
            on_button_a
        )
        await client.start_notify(
            BUTTON_B_UUID,
            on_button_b
        )

        # 5) UART TX (micro:bit → PC) の通知ハンドラ
        await client.start_notify(UART_TX_CHAR_UUID, handle_uart_rx)

        # 6) コマンド送信ループ (UART RX: PC → micro:bit)
        print("\nCommands:\n  [1] ON  → LED ON\n  [2] OFF → LED OFF\n  [q] Quit → 終了")

        # ユーザー入力を非同期で受け取る
        await read_commands(client)

if __name__ == "__main__":
    # 新しいスレッドで非同期イベントループを実行
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
