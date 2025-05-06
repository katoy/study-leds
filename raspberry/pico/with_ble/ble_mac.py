# See 日経ソフトウェア 2925-05

import asyncio
from bleak import BleakScanner, BleakClient

# 定数定義
TARGET_NAME       = "LED-test"
SERVICE_UUID_PART = "181A"
CHARACTERISTIC_UUID = "2ABF"

async def find_device_by_name(name):
    print(f"デバイス名: {name}")
    async with BleakScanner() as scanner:
        await asyncio.sleep(5.0)
        for device in scanner.discovered_devices:
            if device.name == name:
                print(f"MACアドレス: {device.address}")
                return device.address
    print(f"{name} が見つかりません")
    return None

async def find_service_uuid(client, uuid_part):
    for service in client.services:
        if uuid_part.lower() in service.uuid.lower():
            print(f"Service UUID : {service.uuid}")
            return service.uuid
    print("UUID が見つかりません")
    return None

async def interact_with_led(client):
    while True:
        try:
            value = int(input("LED Value (0=OFF / 1=ON): "))
        except ValueError:
            print("数値を入力してください。(0: LED off, 1: LED om. その他: 終了)")
            continue

        if value not in (0, 1):
            print("終了します。")
            break

        data = value.to_bytes(1, 'little')
        await client.write_gatt_char(CHARACTERISTIC_UUID, data, response=True)

async def main():
    address = await find_device_by_name(TARGET_NAME)
    if not address:
        return

    async with BleakClient(address) as client:
        service_uuid = await find_service_uuid(client, SERVICE_UUID_PART)
        if not service_uuid:
            return

        await interact_with_led(client)

if __name__ == "__main__":
    asyncio.run(main())
