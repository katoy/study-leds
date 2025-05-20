import asyncio
from bleak import BleakScanner

async def scan(timeout=5.0):
    devices = await BleakScanner.discover(timeout=timeout)
    for d in devices:
        print(d.name, d.address)
    return devices

asyncio.run(scan())
