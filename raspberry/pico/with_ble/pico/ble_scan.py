# scan_unique.py

import uasyncio as asyncio
import aioble
import bluetooth
from machine import Pin

# GATT Device Name Characteristic UUID
_DEVICE_NAME_CHAR = bluetooth.UUID(0x2A00)

def is_valid(s):
    if not s:
        return False
    for ch in s:
        if ord(ch) < 0x20:
            return False
    return True

# （manual_decode, service_data_decode, mfg_data_decode, read_gatt_name は省略）

async def scan_devices(duration_ms: int = 5000):
    print(f"▶ {duration_ms} ms スキャン開始（アクティブ）")

    # アドレス→(name, RSSI) を保持
    seen = {}

    # Active Scan: duration, interval, window, active を指定
    async with aioble.scan(
        duration_ms,
        interval_us=30000,
        window_us=30000,
        active=True
    ) as scanner:
        async for adv in scanner:
            # アドレス文字列化
            addr = ":".join(f"{b:02X}" for b in adv.device.addr)
            rssi = adv.rssi

            # 名前取得の優先順
            name = None
            try:
                tmp = adv.name()
                if tmp and is_valid(tmp):
                    name = tmp
            except:
                pass

            # Local Name／Service Data／Mfg Data／GATT Name を順に試す
            if not name:
                # raw = adv.adv_data + adv.resp_data ...
                # name = manual_decode(raw) or service_data_decode(raw) or mfg_data_decode(raw)
                # if still None or 'Unknown':
                #     name = await read_gatt_name(adv.device)
                name = "Unknown"  # 省略部分の実装に応じて置き換え

            prev = seen.get(addr)
            # 未登録 or RSSI が強いほうを更新
            if prev is None or rssi > prev[1]:
                seen[addr] = (name, rssi)

    # スキャン後にユニーク一覧だけをプリント
    print("▶ ユニークなデバイス一覧:")
    for addr, (name, rssi) in seen.items():
        print(f"デバイス名: {name}, アドレス: {addr}, RSSI: {rssi}")

async def main():
    await scan_devices(5000)

if __name__ == "__main__":
    asyncio.run(main())
