import asyncio, sys
from bleak import BleakScanner, BleakClient

# 取得した正しいローカル名 or アドレス、またはサービス UUID
TARGET_NAME = "BBC micro:bit"
BUTTON_SERVICE_UUID = "e95d9882-251d-470a-a062-fa1922dfa9a8"
BUTTON_A_UUID       = "e95dda90-251d-470a-a062-fa1922dfa9a8"
BUTTON_B_UUID       = "e95dda91-251d-470a-a062-fa1922dfa9a8"

async def main():
    # 名前フィルタ or サービス UUID フィルタを指定
    device = await BleakScanner.find_device_by_filter(
        lambda d, adv: (adv.local_name and TARGET_NAME in adv.local_name)
                       or BUTTON_SERVICE_UUID in adv.service_uuids,
        timeout=15.0
    )
    if not device:
        print("micro:bit が見つかりませんでした")
        return

    async with BleakClient(device) as client:
        print(f"Connected: {device.address}")
        # 通知ハンドラ設定、A/B ボタンは省略…
        await client.start_notify(BUTTON_A_UUID, lambda _, d: print("A pressed"))
        await client.start_notify(BUTTON_B_UUID, lambda _, d: sys.exit(0))
        await asyncio.Event().wait()  # 永久待機

if __name__ == "__main__":
    asyncio.run(main())
