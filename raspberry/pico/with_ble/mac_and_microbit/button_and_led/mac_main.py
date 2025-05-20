#!/usr/bin/env python3
import asyncio
import sys
from pynput import keyboard  # pynput ライブラリをインポート
from bleak import BleakScanner, BleakClient

# ————————————————————————————————
# デバイス／サービス／キャラクタリスティック UUID
# ————————————————————————————————
TARGET_NAME = "BBC micro:bit"
BUTTON_SERVICE_UUID = "e95d9882-251d-470a-a062-fa1922dfa9a8"
BUTTON_A_UUID = "e95dda90-251d-470a-a062-fa1922dfa9a8"
BUTTON_B_UUID = "e95dda91-251d-470a-a062-fa1922dfa9a8"
UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # write (PC→micro:bit)
UART_TX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # notify (micro:bit→PC)

# —————————————————————————————————
# ボタンA/BおよびUARTのハンドラー
# —————————————————————————————————
async def on_button_a(sender, data):
    print("▶ Button A pressed")

async def on_button_b(sender, data):
    print("▶ Button B pressed - Exiting...")
    loop = asyncio.get_event_loop()
    loop.stop()  # イベントループを停止してプログラムを終了する

async def handle_uart_rx(sender: int, data: bytearray):
    try:
        text = data.decode().strip()
        print(f"⟶ Received UART: {text}")
    except UnicodeDecodeError:
        print(f"⟶ Received raw UART: {data}")

# —————————————————————————————————
# キーボード入力の非同期処理
# —————————————————————————————————
class KeyboardListener:
    def __init__(self):
        self.keys_pressed = set()

    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char:  # key.char がある場合のみ処理
                if key.char in ['1', '2', 'q'] and key.char not in self.keys_pressed:
                    self.keys_pressed.add(key.char)
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if hasattr(key, 'char') and key.char:  # key.char がある場合のみ処理
                if key.char in ['1', '2', 'q'] and key.char in self.keys_pressed:
                    self.keys_pressed.remove(key.char)
            if key == keyboard.Key.esc:
                return False  # ESCキーで終了
        except AttributeError:
            pass

    def start_listener(self):
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

# —————————————————————————————————
# ユーザーコマンドの処理
# —————————————————————————————————
async def read_commands(client, listener):
    while True:
        if '1' in listener.keys_pressed:
            await client.write_gatt_char(UART_RX_CHAR_UUID, b"on\n")
            print("✔ Sent UART: on")
            listener.keys_pressed.remove('1')  # 入力後にセットから削除
        elif '2' in listener.keys_pressed:
            await client.write_gatt_char(UART_RX_CHAR_UUID, b"off\n")
            print("✔ Sent UART: off")
            listener.keys_pressed.remove('2')  # 入力後にセットから削除
        elif 'q' in listener.keys_pressed:
            print("Exiting...")
            break
        await asyncio.sleep(0.1)

# —————————————————————————————————
# メイン処理
# —————————————————————————————————
async def main():
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

    async with BleakClient(device) as client:
        if not client.is_connected:
            print("接続に失敗しました")
            return
        print(f"Connected: {device.address}")

        # サービス一覧を表示（オプション）
        services = await client.get_services()
        print("Discovered services:")
        for srv in services:
            print(f"  • {srv.uuid}")

        # ボタン A/B 通知ハンドラ
        await client.start_notify(BUTTON_A_UUID, on_button_a)
        await client.start_notify(BUTTON_B_UUID, on_button_b)

        # UART TX の通知ハンドラ
        await client.start_notify(UART_TX_CHAR_UUID, handle_uart_rx)

        # キーボードリスナーを開始
        listener = KeyboardListener()
        listener.start_listener()

        # コマンド送信ループ
        print("\nCommands:\n  [1] ON  → LED ON\n  [2] OFF → LED OFF\n  [q] Quit → 終了")
        await read_commands(client, listener)

if __name__ == "__main__":
    asyncio.run(main())
