import machine

# I2C のピン設定
sdaPIN = machine.Pin(0)  # SDAピン (GPIO 0)
sclPIN = machine.Pin(1)  # SCLピン (GPIO 1)

# I2C インターフェースの初期化
i2c = machine.I2C(0, sda=sdaPIN, scl=sclPIN, freq=400000)

# 接続されているデバイスのスキャン
print("Scanning I2C bus...")
devices = i2c.scan()

if len(devices) == 0:
    print("No I2C devices found!")
else:
    print(f"I2C devices found: {len(devices)}")
    for device in devices:
        print(f"Device address: {hex(device)}")  # アドレスを16進数で表示
