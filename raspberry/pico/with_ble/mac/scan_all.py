# See https://af-e.net/python-how-to-use-bleak/#rtoc-9

import asyncio
from bleak import BleakScanner

async def scan_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"デバイス名: {device.name}, アドレス: {device.address}")

# スキャンを実行
asyncio.run(scan_devices())
