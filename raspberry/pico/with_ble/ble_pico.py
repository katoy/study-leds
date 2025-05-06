# See 日経ソフトウェア 2925-05

import asyncio
import aioble
import bluetooth
from machine import Pin

# 定数定義
DEVICE_NAME       = "LED-test"
SERVICE_UUID      = bluetooth.UUID(0x181A)
CHARACTERISTIC_UUID = bluetooth.UUID(0x2ABF)
ADV_APPEARANCE    = 0x04C0
ADV_INTERVAL_MS   = 250_000

def setup_led() -> Pin:
    """内蔵 LED の初期化"""
    return Pin("LED", Pin.OUT)

def setup_gatt_service():
    """GATT サービスとキャラクタリスティックの登録"""
    service = aioble.Service(SERVICE_UUID)
    characteristic = aioble.Characteristic(
        service,
        CHARACTERISTIC_UUID,
        write=True,
        notify=True
    )
    aioble.register_services(service)
    return characteristic

async def handle_led_control(characteristic, led: Pin):
    """キャラクタリスティックの書き込みに応じて LED を制御"""
    while True:
        await characteristic.written()
        msg = characteristic.read()
        if msg:
            state = msg[0]
            print("LED state =", state)
            led.value(state)
        await asyncio.sleep_ms(100)

async def advertise_and_wait_connection():
    """アドバタイズして接続を待機"""
    while True:
        async with await aioble.advertise(
            ADV_INTERVAL_MS,
            name=DEVICE_NAME,
            services=[SERVICE_UUID],
            appearance=ADV_APPEARANCE,
        ) as connection:
            print("Connected from", connection.device)
            await connection.disconnected()

async def main():
    led = setup_led()
    led.on()  # 起動時に LED 点灯

    characteristic = setup_gatt_service()

    await asyncio.gather(
        handle_led_control(characteristic, led),
        advertise_and_wait_connection()
    )

asyncio.run(main())
