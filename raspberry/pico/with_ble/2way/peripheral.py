import uasyncio as asyncio
import aioble
from machine import Pin
from config import (
    SERVICE_UUID,
    CHARACTERISTIC_UUID,
    LED_PIN,
    DEVICE_NAME,
    encode_message,
    decode_message,
)

# ── ハードウェア設定 ────────────────────────────
led = Pin(LED_PIN, Pin.OUT)

# ── GATT サービス／キャラクタリスティック設定 ───
svc = aioble.Service(SERVICE_UUID)
char = aioble.Characteristic(
    svc,
    CHARACTERISTIC_UUID,
    read=True,
    write=True,
    notify=True,
)
# 初期状態を「Off」でセット
char.value = encode_message("Off")
aioble.register_services(svc)

async def handle_central_writes(conn):
    """
    Central からの書き込みを待ち、LED トグル＆ステータス返送。
    CancelledError はキャッチしてここで終了させる。
    """
    try:
        while conn.is_connected():
            await char.written()
            buf = char.read()
            command = decode_message(buf)
            print(f"Peripheral: received write payload: {command}")

            if command == "toggle":
                led.toggle()
                led_state = "On" if led.value() else "Off"

                # char.value を更新 (Central の read() 用)
                char.write(encode_message(led_state))
                print(f"Peripheral: LED toggled to : {led_state}")

    except asyncio.CancelledError:
        print("Peripheral: write handler cancelled")
        # ここで swallow して coroutine を終了
    except Exception as e:
        print(f"Peripheral: error in write handler: {e}")

async def main():
    """
    永久ループで
      広告 → 接続待ち → 書き込みハンドラ起動 → 切断 → ハンドラ停止 → 再広告
    を繰り返す。
    """
    while True:
        conn = await aioble.advertise(
            interval_us=250_000,
            name=DEVICE_NAME,
            services=[SERVICE_UUID],
        )
        print("Peripheral: connected to central!")

        task = asyncio.create_task(handle_central_writes(conn))

        try:
            # 切断されるまで待機
            while conn.is_connected():
                await asyncio.sleep_ms(100)
        finally:
            # 切断時にハンドラをキャンセルして終了を待つ
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

            print("Peripheral: central disconnected, restarting advertising…")

# エントリポイント
asyncio.run(main())
