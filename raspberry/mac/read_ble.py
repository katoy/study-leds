import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_NAME = "PicoTempSensor"
CHAR_UUID = "00002a6e-0000-1000-8000-00805f9b34fb"  # BLE キャラクタリスティック UUID
SCAN_TIMEOUT = 10  # スキャンタイムアウト (秒)
MAX_RETRIES = 3    # 再試行回数

async def notification_handler(sender, data: bytearray):
    """
    BLE 通知を処理するコールバック関数。
    Args:
        sender: データを送信したキャラクタリスティックのハンドル。
        data: 受信したデータ（bytearray）。
    """
    print(f"Received: {data.decode('utf-8').strip()}")

async def find_device():
    """
    デバイスをスキャンして名前に一致するデバイスを返す。
    Returns:
        BLE デバイスオブジェクト (成功時) または None (失敗時)。
    """
    print(f"Scanning for BLE device with name '{DEVICE_NAME}'...")
    devices = await BleakScanner.discover(timeout=SCAN_TIMEOUT)
    for device in devices:
        if device.name == DEVICE_NAME:
            print(f"Found target device: {device.name}, Address: {device.address}")
            return device
    print(f"Device with name '{DEVICE_NAME}' not found.")
    return None

async def connect_to_device(device):
    """
    デバイスに接続し、通知を受信する。
    Args:
        device: BLE デバイスオブジェクト。
    """
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            async with BleakClient(device.address) as client:
                if not client.is_connected:
                    raise Exception(f"Failed to connect to {device.name}")

                print(f"Connected to {device.name}. Starting notifications...")
                await client.start_notify(CHAR_UUID, notification_handler)

                # 接続維持中はループ
                while client.is_connected:
                    await asyncio.sleep(1)
                print("Disconnected from device.")
                return
        except Exception as e:
            retry_count += 1
            print(f"Retry {retry_count}/{MAX_RETRIES} failed: {e}")
            await asyncio.sleep(2)  # 再試行前に待機
    print(f"Failed to connect to {device.name} after {MAX_RETRIES} retries.")

async def main():
    """
    メイン処理。デバイスを探して接続を試みる。
    """
    while True:
        device = await find_device()
        if device:
            await connect_to_device(device)
        print("Retrying scan...")
        await asyncio.sleep(5)  # 再スキャンまでの待機時間

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")

