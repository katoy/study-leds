"""
Raspberry Pi Pico W の BLE サーバーとして動作し、
現在の日時（JST）と CPU 温度を定期的に送信します。
"""

import bluetooth
import struct
from machine import Timer, RTC
from picozero import pico_temp_sensor
import ntptime
import time
import network


class BLETemperatureServer:
    """
    BLE を使用して現在の日付と時刻（JST）、および CPU 温度を送信するクラス。
    """
    IRQ_CENTRAL_CONNECT = 1
    IRQ_CENTRAL_DISCONNECT = 2

    def __init__(self, name="PicoTempSensor", interval=2000):
        """
        初期化メソッド。
        Args:
            name (str): BLE デバイス名。
            interval (int): データ送信間隔（ミリ秒）。
        """
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.irq(self._irq_handler)

        self.name = name
        self.interval = interval

        # サービス UUID とキャラクタリスティック UUID
        self._temp_service_uuid = bluetooth.UUID("0000181a-0000-1000-8000-00805f9b34fb")
        self._temp_char_uuid = bluetooth.UUID("00002a6e-0000-1000-8000-00805f9b34fb")

        self._temp_char = (
            self._temp_char_uuid,
            bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY,
        )
        self._temp_service = (
            self._temp_service_uuid,
            (self._temp_char,),
        )

        self._services = (self._temp_service,)
        ((self._temp_handle,),) = self.ble.gatts_register_services(self._services)

        self._connected = False
        self._conn_handle = None

        self.rtc = RTC()

        # Wi-Fi に接続
        self._connect_to_wifi()

        # 時刻を初期化
        self._initialize_time()

        self._timer = Timer(-1)
        self._timer.init(period=self.interval, mode=Timer.PERIODIC, callback=self._send_data)

        self.ble.config(gap_name=self.name)
        self._advertise()

        # 起動時の情報を表示
        print(f"BLE デバイス名: {self.name}")
        print(f"サービス UUID: {self._temp_service_uuid}")
        print(f"キャラクタリスティック UUID: {self._temp_char_uuid}")

    def _connect_to_wifi(self):
        """
        Wi-Fi に接続する。
        """
        try:
            with open("config.txt") as f:
                lines = f.readlines()
            config = {line.split("=")[0].strip(): line.split("=")[1].strip() for line in lines}
            ssid = config.get("SSID")
            password = config.get("PASSWORD")

            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.connect(ssid, password)

            print(f"Wi-Fi に接続中: {ssid}")
            while not wlan.isconnected():
                time.sleep(1)

            print(f"Wi-Fi 接続成功: {wlan.ifconfig()}")
        except Exception as e:
            print(f"Wi-Fi 接続エラー: {e}")
            raise e

    def _initialize_time(self):
        """
        NTP サーバーを使用して時刻を同期し、JST に設定。
        """
        try:
            ntptime.host = "129.6.15.28"  # IP を直接指定
            ntptime.settime()
            current_time = time.localtime(time.time() + 9 * 3600)  # UTC -> JST
            self.rtc.datetime((
                current_time[0], current_time[1], current_time[2],
                current_time[6], current_time[3], current_time[4],
                current_time[5], 0
            ))
            print(f"現在の JST 時刻: {self._get_formatted_time()}")
        except Exception as e:
            print(f"NTP 時刻の同期に失敗しました: {e}")
            print("RTC 時刻を手動で設定してください。")

    def _get_formatted_time(self):
        """
        現在の日時を 'YYYY-MM-DD HH:MM:SS' フォーマットで返す。
        """
        current_time = self.rtc.datetime()
        return f"{current_time[0]:04}-{current_time[1]:02}-{current_time[2]:02} {current_time[4]:02}:{current_time[5]:02}:{current_time[6]:02}"

    def _irq_handler(self, event, data):
        if event == self.IRQ_CENTRAL_CONNECT:
            self._conn_handle, _, _ = data
            print(f"中央デバイスが接続しました (ハンドル: {self._conn_handle})")
            self._connected = True
        elif event == self.IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print(f"中央デバイスが切断されました (ハンドル: {conn_handle})")
            self._connected = False
            self._conn_handle = None
            self._advertise()

    def _advertise(self):
        """
        BLE アドバタイズを開始する。
        """
        name_bytes = self.name.encode("utf-8")
        adv_data = struct.pack(
            "BB6sBB", 
            2, 0x01, b'\x06',  # フラグ: General Discoverable Mode | BR/EDR Not Supported
            len(name_bytes) + 1, 0x09  # 完全なローカル名
        ) + name_bytes

        self.ble.gap_advertise(100, adv_data)
        print(f"アドバタイズを開始しました: {self.name}")

    def _send_data(self, t):
        """
        現在の日時（JST）と温度を送信。
        """
        if not self._connected or self._conn_handle is None:
            return

        try:
            temperature = pico_temp_sensor.temp
            timestamp = self._get_formatted_time()
            data_str = f"{timestamp}, {temperature:.2f}\n"
            data_bytes = data_str.encode("utf-8")

            print(f"送信データ: {data_str.strip()}")
            self.ble.gatts_write(self._temp_handle, data_bytes)
            self.ble.gatts_notify(self._conn_handle, self._temp_handle, data_bytes)
        except Exception as e:
            print(f"データ送信エラー: {e}")

    def stop(self):
        """
        BLE サーバーを停止する。
        """
        self._timer.deinit()
        self.ble.active(False)
        print("BLE サーバーを停止しました。")


if __name__ == "__main__":
    try:
        print("BLE 温度センサープログラムを開始します。")
        server = BLETemperatureServer(name="PicoTempSensor", interval=2000)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nプログラムを終了します。")
        server.stop()
