# scan_unique.py

import uasyncio as asyncio
import aioble
import bluetooth

# GATT Device Name Characteristic UUID
_DEVICE_NAME_CHAR = bluetooth.UUID(0x2A00)

def is_valid(s: str) -> bool:
    """制御文字なし＆空文字でないかチェック"""
    if not s:
        return False
    for ch in s:
        if ord(ch) < 0x20:
            return False
    return True

def parse_ad_structures(data: bytes):
    """TLV を (ad_type, value_bytes) のリストに分解"""
    results = []
    i = 0
    length = len(data)
    while i < length:
        adv_len = data[i]
        # 長さ 0 か範囲外なら終了
        if adv_len == 0 or i + adv_len >= length:
            break
        ad_type = data[i + 1]
        value   = data[i + 2 : i + 1 + adv_len]
        results.append((ad_type, value))
        i += adv_len + 1
    return results

def decode_name_from_tlv(data: bytes) -> str | None:
    """AD Type 0x08/0x09 (Local Name) を探す"""
    for ad_type, val in parse_ad_structures(data):
        if ad_type in (0x08, 0x09):
            try:
                name = val.decode('utf-8', 'ignore')
                if is_valid(name):
                    return name
            except:
                pass
    return None

def decode_service_data(data: bytes) -> str | None:
    """AD Type 0x16,0x20,0x21 の Service Data を探す"""
    for ad_type, val in parse_ad_structures(data):
        if ad_type in (0x16, 0x20, 0x21):
            try:
                name = val.decode('utf-8', 'ignore')
                if is_valid(name):
                    return name
            except:
                pass
    return None

def decode_manufacturer_data(data: bytes) -> str | None:
    """
    AD Type 0xFF 内の英字／スペースが4文字以上連続するシーケンスを抽出
    （ノイズ排除のため4文字以上に制限）
    """
    seq = b''
    for b in data:
        if (0x41 <= b <= 0x5A) or (0x61 <= b <= 0x7A) or b == 0x20:
            seq += bytes([b])
            if len(seq) >= 4:
                try:
                    name = seq.decode('utf-8', 'ignore').strip()
                    if is_valid(name):
                        return name
                except:
                    pass
        else:
            seq = b''
    return None

async def read_gatt_name(device) -> str | None:
    """スキャン後の Unknown に対して GATT 0x2A00 を読み取り"""
    try:
        conn = await aioble.connect(device, timeout_ms=2000)
        async with conn:
            raw = await conn.read_gatt_char(_DEVICE_NAME_CHAR)
            name = raw.decode('utf-8', 'ignore').split('\x00', 1)[0]
            if is_valid(name):
                return name
    except:
        pass
    return None

async def scan_devices(duration_ms: int = 5000):
    print(f"▶ {duration_ms} ms スキャン開始（アクティブ）")
    seen: dict[str, tuple] = {}

    # ── 第1段階: ADV／ScanResponse から４種類の情報で名前抽出 ──
    async with aioble.scan(
        duration_ms,
        interval_us=30000,
        window_us=30000,
        active=True
    ) as scanner:
        async for adv in scanner:
            addr = ":".join(f"{b:02X}" for b in adv.device.addr)
            rssi = adv.rssi

            # 生データをまとめる
            adv_data = bytes(adv.adv_data) if adv.adv_data else b''
            resp_data = bytes(adv.resp_data) if adv.resp_data else b''
            packet = adv_data + resp_data

            name = None

            # 1) aioble 組み込み adv.name()
            try:
                tmp = adv.name()
                if tmp and is_valid(tmp):
                    name = tmp
            except:
                pass

            # 2) TLV の Local Name (0x08/0x09)
            if not name:
                name = decode_name_from_tlv(packet)

            # 3) Service Data (0x16,0x20,0x21)
            if not name:
                name = decode_service_data(packet)

            # 4) Manufacturer Data (0xFF)
            if not name and adv.adv_data:
                name = decode_manufacturer_data(adv_data)

            if not name:
                name = "Unknown"

            prev = seen.get(addr)
            # RSSI が強いものを残す
            if prev is None or rssi > prev[2]:
                seen[addr] = (adv.device, name, rssi)

    # ── 第2段階: Unknown のみ GATT 読み取りで再トライ ──
    for addr, (device, name, rssi) in list(seen.items()):
        if name == "Unknown":
            new_name = await read_gatt_name(device)
            if new_name:
                print(f"  ↳ {addr} を GATT 読み取り → {new_name}")
                seen[addr] = (device, new_name, rssi)

    # ── 結果表示 ──
    print("▶ ユニークなデバイス一覧:")
    for addr, (_, name, rssi) in seen.items():
        print(f"デバイス名: {name}, アドレス: {addr}, RSSI: {rssi}")

async def main():
    await scan_devices(5000)

if __name__ == "__main__":
    asyncio.run(main())
