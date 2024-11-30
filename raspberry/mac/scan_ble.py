import asyncio
from bleak import BleakScanner

async def scan():
    print("Scanning for BLE devices (10 seconds)...")
    devices = await BleakScanner.discover(timeout=10)  # スキャン時間を 10 秒に延長
    if not devices:
        print("No BLE devices found.")
        return
    for device in devices:
        print(f"Device: {device.name or 'Unknown'}, Address: {device.address}")

try:
    asyncio.run(scan())
except Exception as e:
    print(f"Error during BLE scan: {e}")

