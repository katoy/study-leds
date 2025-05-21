#!/usr/bin/env python3
import asyncio
from pynput import keyboard
from bleak import BleakScanner, BleakClient

# ————————————————————————————————
# デバイス／サービス／キャラクタリスティック UUID
# ————————————————————————————————
TARGET_NAME        = "BBC micro:bit"
UART_SERVICE_UUID  = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID  = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # write (PC→micro:bit)
UART_TX_CHAR_UUID  = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # notify (micro:bit→PC)

# —————————————————————————————————
# グローバルな終了イベント
# —————————————————————————————————
exit_event = asyncio.Event()

# —————————————————————————————————
# UART 受信ハンドラ
# —————————————————————————————————
def handle_uart_rx(_: int, data: bytearray):
    text = data.decode(errors="ignore").strip()
    if text == "A":
        print("⟶ micro:bit Button A pressed")
    elif text == "B":
        print("⟶ micro:bit Button B pressed — Exiting…")
        exit_event.set()  # フラグを立てるだけ
    else:
        print(f"⟶ Received UART: {text}")

# —————————————————————————————————
# キーボード入力リスナー
# —————————————————————————————————
class KeyboardListener:
    def __init__(self):
        self.keys = set()

    def on_press(self, key):
        try:
            if key.char in ["1", "2", "q"]:
                self.keys.add(key.char)
        except AttributeError:
            pass

    def on_release(self, key):
        # ESC でも終了フラグを立てる
        if key == keyboard.Key.esc:
            exit_event.set()
            return False

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.daemon = True
        listener.start()

# —————————————————————————————————
# キーボードから micro:bit へ送信
# —————————————————————————————————
async def send_commands(client, listener):
    while not exit_event.is_set():
        if "1" in listener.keys:
            await client.write_gatt_char(UART_RX_CHAR_UUID, b"on\n")
            print("✔ Sent UART: on")
            listener.keys.remove("1")
        elif "2" in listener.keys:
            await client.write_gatt_char(UART_RX_CHAR_UUID, b"off\n")
            print("✔ Sent UART: off")
            listener.keys.remove("2")
        elif "q" in listener.keys:
            print("Exiting by keyboard…")
            exit_event.set()
            listener.keys.remove("q")
        await asyncio.sleep(0.1)

# —————————————————————————————————
# メイン処理
# —————————————————————————————————
async def main():
    print("Scanning for micro:bit (UART service)…")
    device = await BleakScanner.find_device_by_filter(
        lambda d, adv: (
            adv.local_name and TARGET_NAME in adv.local_name
        ) or (
            UART_SERVICE_UUID in (adv.service_uuids or [])
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

        # UART TX 通知を開始
        await client.start_notify(UART_TX_CHAR_UUID, handle_uart_rx)

        # キーボードリスナー開始
        listener = KeyboardListener()
        listener.start()

        print("\nCommands:\n  [1] ON  → micro:bit に “on” 送信\n  [2] OFF → micro:bit に “off” 送信\n  [q]/ESC → 終了")
        # 送信ループと終了フラグ待ちを同時に実行
        await asyncio.gather(
            send_commands(client, listener),
            exit_event.wait()
        )

        # クリーンアップ
        await client.stop_notify(UART_TX_CHAR_UUID)
        print("Disconnected.")

if __name__ == "__main__":
    asyncio.run(main())
