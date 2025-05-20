#!/usr/bin/env python3
import asyncio
from bleak import BleakScanner, BleakClient

# UUIDs for Nordic UART Service (NUS)
UART_SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
UART_RX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # write
UART_TX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # notify

async def run():
    # 1) 全デバイスをスキャンして AdvertisementData を取得
    print("Scanning for micro:bit...")
    devices = await BleakScanner.discover(timeout=5.0, return_adv=True)

    target = None
    for device, adv in devices.values():
        name = device.name or adv.local_name or ""
        if "micro:bit" in name:
            print(f"Found {name} @ {device.address}")
            target = device
            break

    if not target:
        print("micro:bit not found.")
        return

    # 2) micro:bit に接続
    async with BleakClient(target.address) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        print(f"Connected to micro:bit @ {target.address}")

        # 3) オプション: サービス一覧を表示して確認
        services = await client.get_services()
        print("Discovered services:")
        for srv in services:
            print(f"  • {srv.uuid}")

        # 4) UART TX (notify) をサブスクライブして受信ハンドラを設定
        def handle_rx(sender: int, data: bytearray):
            try:
                text = data.decode().strip()
                print(f"Received: {text}")
            except UnicodeDecodeError:
                print(f"Received raw: {data}")

        await client.start_notify(UART_TX_CHAR_UUID, handle_rx)

        # 5) コマンド送信ループ
        while True:
            choice = input("[1] ON   [2] OFF   [q] Quit > ").strip().lower()
            if choice == "1":
                await client.write_gatt_char(UART_RX_CHAR_UUID, b"on\n")
                print("Sent: on")
            elif choice == "2":
                await client.write_gatt_char(UART_RX_CHAR_UUID, b"off\n")
                print("Sent: off")
            elif choice == "q":
                print("Exiting.")
                break
            else:
                print("Invalid selection.")

        # 6) クリーンアップ
        await client.stop_notify(UART_TX_CHAR_UUID)

if __name__ == "__main__":
    asyncio.run(run())
