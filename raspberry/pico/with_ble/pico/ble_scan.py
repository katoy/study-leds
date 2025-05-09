import uasyncio as asyncio
import aioble
import bluetooth

# 汎用 BLE スキャナー：Active Scan + 名前取得 + GATT Device Name読み取り
# • adv.name() → AD Local Name → Service Data → Manufacturer Data → GATT Device Name
# • 制御文字を排除 (control characters only)
# • adv_data/advertising_data, resp_data/scan_response に対応

# GATT Device Name キャラクタリスティック UUID
_DEVICE_NAME_CHAR = bluetooth.UUID(0x2A00)


def is_valid(s):
    """
    制御文字以外を許容 (Unicode printable)。空文字は無効。
    """
    if not s:
        return False
    for ch in s:
        code = ord(ch)
        # 0x20 以上なら制御文字ではない
        if code < 0x20:
            return False
    return True


def manual_decode(raw):
    """AD の Local Name (0x09/0x08) を抽出し、制御文字を排除"""
    i, fallback = 0, None
    L = len(raw)
    while i + 1 < L:
        fld = raw[i]
        if fld < 2 or i + 1 + fld > L:
            break
        ad_type = raw[i+1]
        chunk = raw[i+2:i+1+fld].rstrip(b"\x00")
        try:
            name = chunk.decode("utf-8","ignore").strip()
        except:
            name = None
        if ad_type == 0x09 and is_valid(name):
            return name
        if ad_type == 0x08 and fallback is None and is_valid(name):
            fallback = name
        i += fld + 1
    return fallback


def service_data_decode(raw):
    """Service Data (0x16) のペイロード部分を抽出し、制御文字を排除"""
    i, L = 0, len(raw)
    while i + 1 < L:
        fld = raw[i]
        if fld < 3 or i + 1 + fld > L:
            break
        ad_type = raw[i+1]
        if ad_type == 0x16:
            sd = raw[i+2:i+1+fld]
            text = sd[2:]
            try:
                s = text.decode("utf-8","ignore").strip()
            except:
                s = None
            if is_valid(s):
                return s
        i += fld + 1
    return None


def mfg_data_decode(raw):
    """Manufacturer Data (0xFF) のペイロード部分を抽出し、制御文字を排除"""
    i, L = 0, len(raw)
    while i + 1 < L:
        fld = raw[i]
        if fld < 3 or i + 1 + fld > L:
            break
        ad_type = raw[i+1]
        if ad_type == 0xFF:
            md = raw[i+2:i+1+fld]
            text = md[2:] if len(md)>2 else md
            try:
                s = text.decode("utf-8","ignore").strip()
            except:
                s = None
            if is_valid(s):
                return s
        i += fld + 1
    return None

async def read_gatt_name(device):
    """GATT Device Name (0x2A00) を読み取る"""
    addr_bytes = bytes(device.addr)
    addr_type = getattr(device, 'addr_type', 0)
    try:
        async with aioble.connect(addr_bytes, addr_type) as conn:
            data = await conn.read_gatt_char(_DEVICE_NAME_CHAR)
            name = data.decode('utf-8', 'ignore').strip()
            if is_valid(name):
                return name
    except Exception:
        pass
    return None

async def scan_devices(duration_ms: int = 5000):
    print(f"▶ {duration_ms} ms スキャン開始（アクティブ）")
    seen = {}

    async with aioble.scan(duration_ms, 1) as scanner:
        async for adv in scanner:
            addr = ":".join(f"{b:02X}" for b in adv.device.addr)
            rssi = adv.rssi
            adv_bytes = getattr(adv, 'adv_data', None) or getattr(adv, 'advertising_data', None) or b''
            resp_bytes = getattr(adv, 'resp_data', None) or getattr(adv, 'scan_response', None) or b''
            raw = adv_bytes + resp_bytes

            # 1) aioble 内蔵 name()
            try:
                name = adv.name()
            except Exception:
                name = None
            if not (name and is_valid(name)):
                name = None

            # 2) AD Local Name
            if not name:
                name = manual_decode(raw)

            # 3) Service Data
            if not name:
                name = service_data_decode(raw)

            # 4) Manufacturer Data
            if not name:
                name = mfg_data_decode(raw)

            # 5) GATT Device Name
            if not name or name == 'Unknown':
                gatt_name = await read_gatt_name(adv.device)
                if gatt_name:
                    name = gatt_name

            if not name:
                name = 'Unknown'

            prev = seen.get(addr)
            if (prev is None or rssi > prev[1] or (prev[0]=='Unknown' and name!='Unknown')):
                seen[addr] = (name, rssi)

    print("▶ Scan 結果:")
    for addr, (name, rssi) in seen.items():
        print(f"デバイス名: {name}, アドレス: {addr}, RSSI: {rssi}")

if __name__ == '__main__':
    asyncio.run(scan_devices(5000))
