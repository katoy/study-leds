# See https://af-e.net/python-how-to-use-bleak/#rtoc-9

import asyncio
from bleak import BleakScanner
async def scan_specific_device(target_name):
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name == target_name:
            print(f"特定デバイス: {device.name}, アドレス: {device.address}")

# 特定のデバイス名を指定してスキャン
asyncio.run(scan_specific_device("Device1"))
