# central.py

import uasyncio as asyncio
import aioble
from machine import Pin
from config import (
    SERVICE_UUID,
    CHARACTERISTIC_UUID,
    BUTTON_PIN,
    LED_PIN,
    DEVICE_NAME,
    encode_message,
    decode_message,
)

# ── ハードウェア設定 ────────────────────────────
led    = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# ── BLE スキャンパラメータ ────────────────────────
SCAN_TIMEOUT_MS   = 5000     # スキャン継続時間（ms）
SCAN_INTERVAL_US  = 30_000   # スキャンインターバル（μs）
SCAN_WINDOW_US    = 30_000   # スキャン窓（μs）
SCAN_ACTIVE       = True     # アクティブスキャンの有無

async def handle_connection(conn):
    """
    接続確立後の制御ループ。
    ボタン押下で write → read で LED 同期 → 切断時に自動クリーンアップ。
    """
    try:
        svc = await conn.service(SERVICE_UUID)
        if svc is None:
            print("Error: Service not found")
            return

        char = await svc.characteristic(CHARACTERISTIC_UUID)
        if char is None:
            print("Error: Characteristic not found")
            return

        print("Central: entering control loop")
        last = button.value()

        while conn.is_connected():
            await asyncio.sleep_ms(50)
            val = button.value()
            if last == 1 and val == 0:
                command = "toggle"
                await char.write(encode_message(command))
                print(f"Central: write sent: '{command}'")

                data = await char.read()
                remote_state = decode_message(data)
                print(f" ---- remote LED: {remote_state}")

            last = val

    except Exception as e:
        print(f"Central: connection error: {e}")
    finally:
        print("Central: connection handler exiting")
        await conn.disconnect()

async def scan_and_connect():
    """
    スキャン → 発見 → 接続 → handle_connection をバックグラウンドタスクで起動 → 再スキャン
    を繰り返す。
    """
    # 実行中の接続ハンドラを管理するためのセット
    active_tasks = set()

    while True:
        print(f"Central: scanning for {DEVICE_NAME} …")
        async with aioble.scan(
            SCAN_TIMEOUT_MS,
            SCAN_INTERVAL_US,
            SCAN_WINDOW_US,
            SCAN_ACTIVE
        ) as scanner:
            async for adv in scanner:
                if adv.name() == DEVICE_NAME:
                    print(f"Central: found peripheral, RSSI={adv.rssi}")

                    try:
                        conn = await adv.device.connect(timeout_ms=5000)
                        print("Central: connected")

                        # handle_connection をバックグラウンドで実行
                        task = asyncio.create_task(handle_connection(conn))
                        active_tasks.add(task)

                        # タスク完了後にセットから除外
                        task.add_done_callback(lambda t: active_tasks.discard(t))

                    except Exception as e:
                        print(f"Central: connect failed: {e}")

                    # 接続処理をバックグラウンドに移譲したのでスキャンを抜ける
                    break

        # 短時間待機して次のスキャンへ
        await asyncio.sleep_ms(500)

def main():
    asyncio.run(scan_and_connect())

if __name__ == "__main__":
    main()
