import bluetooth

# ── 共通 UUID ───────────────────────────────────
SERVICE_UUID        = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")

# ── デバイス／GPIO 設定 ───────────────────────────
DEVICE_NAME = "PICO-PERIP"
BUTTON_PIN  = 16
LED_PIN     = "LED"   # Pico W の内蔵 LED

# ── ユーティリティ ─────────────────────────────────
def encode_message(message: str) -> bytes:
    """文字列を UTF-8 でエンコードして返す"""
    return message.encode('utf-8')

def decode_message(payload: bytes) -> str:
    """バイト列を UTF-8 でデコードして文字列として返す"""
    return payload.decode('utf-8')
