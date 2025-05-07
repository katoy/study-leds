# Raspberry Pi Pico W LED 制御クライアント

このプロジェクトは、Raspberry Pi Pico W（または Pico 2 W）上で動作する BLE GATT サーバーに対して、Web ブラウザ（Chrome）の Web Bluetooth API を利用して本体内蔵 LED の ON/OFF 制御を行うサンプルアプリケーションです。

---

## ディレクトリ構成

```
project-root/
├── index.html           # ブラウザ用 UI
├── js/
│   └── app.js           # ES モジュール化した制御ロジック
├── __tests__/
│   └── app.test.js      # Jest による単体テスト
├── babel.config.cjs     # Babel 設定（CommonJS）
├── jest.config.cjs      # Jest 設定（CommonJS）
├── package.json         # npm プロジェクト定義
└── README.md            # 本書
```

---

## 必要な環境

* Node.js (推奨バージョン 14 以上)
* npm
* Python 3 （ローカル HTTP サーバー起動用）
* 最新の Chrome（Web Bluetooth API 対応）

---

## 実機動作手順

1. **Raspberry Pi Pico W にファームウェアを書き込み**

   * MicroPython + aioble ライブラリをセットアップし、以下のサンプルコードを Pico に転送して実行してください。

   ```python
   import asyncio
   import aioble
   import bluetooth
   from machine import Pin

   DEVICE_NAME       = "LED-test"
   SERVICE_UUID      = bluetooth.UUID(0x181A)
   CHARACTERISTIC_UUID = bluetooth.UUID(0x2ABF)
   ADV_APPEARANCE    = 0x04C0
   ADV_INTERVAL_MS   = 250_000

   def setup_led():
       return Pin("LED", Pin.OUT)

   def setup_gatt_service():
       service = aioble.Service(SERVICE_UUID)
       char = aioble.Characteristic(
           service,
           CHARACTERISTIC_UUID,
           write=True,
           notify=True
       )
       aioble.register_services(service)
       return char

   async def handle_led_control(char, led):
       while True:
           await char.written()
           msg = char.read()
           if msg:
               led.value(msg[0])
           await asyncio.sleep_ms(100)

   async def advertise_and_wait_connection():
       while True:
           async with await aioble.advertise(
               ADV_INTERVAL_MS,
               name=DEVICE_NAME,
               services=[SERVICE_UUID],
               appearance=ADV_APPEARANCE
           ) as connection:
               await connection.disconnected()

   async def main():
       led = setup_led()
       led.on()
       char = setup_gatt_service()
       await asyncio.gather(
           handle_led_control(char, led),
           advertise_and_wait_connection()
       )

   asyncio.run(main())
   ```

2. **ローカル HTTP サーバーを起動**
   プロジェクトルートで HTML/JS を HTTP 経由で提供します。

   ```bash
   cd project-root
   python3 -m http.server 8000
   ```

   または npm の `live-server` などでも構いません。
   ブラウザで `http://localhost:8000/index.html` を開いてください。

3. **ブラウザで接続**

   * Chrome のアドレスバーに `http://localhost:8000/index.html` を入力してページを表示
   * 「接続」ボタンを押し、デバイス名 `LED-test` の Pico W を選択
   * 「LED ON」「LED OFF」「切断」ボタンで動作を確認

---

## テスト実行方法

Jest を使った単体テストが用意されています。以下の手順で実行してください。

```bash
# 依存パッケージをインストール
npm install

# テスト実行
npm test
```

テストファイルは `__tests__/app.test.js` にあり、UI 更新ロジックや接続モックの振る舞いを検証します。

---

## カバレッジ計測方法

Jest のカバレッジ機能を利用します。`package.json scripts` に定義した `coverage` コマンドで計測・レポート生成が可能です。

```bash
# カバレッジ計測実行
npm run coverage
```

* レポートは `coverage/lcov-report/index.html` に出力されます。
* `README.md` と同階層の `coverage` フォルダを開いてブラウザで確認してください。

---

以上でセットアップと実行方法の説明は完了です。何か問題があれば Issue を立ててください。
