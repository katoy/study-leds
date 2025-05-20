import asyncio
from bleak import BleakScanner

async def debug_scan():
    print("全デバイスをスキャン中…")
    devices = await BleakScanner.discover(timeout=5.0)
    for d in devices:
        print(f"{d.name!r} @ {d.address} → {d.metadata.get('uuids')}")
    print("完了。")

if __name__ == "__main__":
    asyncio.run(debug_scan())
