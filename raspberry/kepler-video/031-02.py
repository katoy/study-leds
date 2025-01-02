"""
このプログラムは、日本の気象庁APIから天気データを取得し、
SSD1306 OLED ディスプレイにリアルタイムで表示するためのものです。

主な機能:
1. Wi-Fi の接続情報を設定ファイルから読み込みます。
2. Wi-Fi に接続して、指定した間隔で天気データを取得します。
3. 取得した天気情報 (天気の説明、気温、湿度) を OLED ディスプレイに表示します。
4. 表示内容には日本時間 (UTC+9) が含まれます。
5. 長いテキストは自動で折り返してディスプレイに表示します。
6. プログラム終了時にリソースを適切に解放します。

使用方法:
1. `config.txt` に Wi-Fi の SSID、パスワードを記載してください。
2. SSD1306 OLED ディスプレイを I2C 接続 (GPIO 0: SDA, GPIO 1: SCL) で接続してください。
3. スクリプトを実行すると、天気情報がリアルタイムで表示されます。
"""

import network
import urequests
import time
import machine
import ssd1306
import xml.etree.ElementTree as ET

# 定数
REGION_CODE = "130000"  # 地域コード (例: 東京都)
UPDATE_INTERVAL = 60 * 10  # 更新間隔 (秒)
JMA_API_URL = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{REGION_CODE}.json"

# I2C 設定
i2c = machine.I2C(1, scl=machine.Pin(3), sda=machine.Pin(2), freq=200000)  # SDA: GPIO2, SCL: GPIO3
display = ssd1306.SSD1306_I2C(128, 64, i2c)


def load_config(file_path='config.txt'):
    """設定ファイルを読み込みます。"""
    config = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        print(f"エラー: {file_path} が見つかりませんでした。")
    except Exception as e:
        print(f"設定ファイル読み込み中の予期しないエラー: {e}")
    machine.reset()


def connect_to_wifi(ssid, password, max_retries=10):
    """Wi-Fi ネットワークに接続します。"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print(f"Wi-Fi SSID: {ssid} に接続中...")
    wlan.connect(ssid, password)

    for retry in range(max_retries):
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f"Wi-Fi に正常に接続しました。IP アドレス: {ip}")
            return ip
        print(f"再接続を試みています... ({retry + 1}/{max_retries})")
        time.sleep(1)

    print("複数回試行しましたが、Wi-Fi 接続に失敗しました。")
    raise RuntimeError("Wi-Fi 接続に失敗しました")


def get_weather():
    """気象庁APIから天気データを取得します。"""
    try:
        print("気象庁APIからデータを取得中...")
        res = urequests.get(JMA_API_URL)
        if res.status_code != 200:
            print(f"エラー: HTTP ステータスコード {res.status_code}")
            return None

        # JSON データを解析
        weather_data = res.json()
        today_forecast = weather_data[0]['timeSeries'][0]['areas'][0]

        description = today_forecast['weathers'][0]  # 天気の説明
        temperature = weather_data[1]['timeSeries'][1]['areas'][0]['temps'][0]  # 気温

        return description, temperature
    except Exception as e:
        print(f"エラー: 天気データ取得中に問題が発生しました: {e}")
        return None


def display_weather(description, temperature):
    """天気データをSSD1306ディスプレイに表示します。"""
    display.fill(0)
    display.text(f"Weather: {description}", 0, 0)
    display.text(f"Temp: {temperature} C", 0, 16)
    display.show()


def main():
    """メインプログラムループ。"""
    try:
        config = load_config()
        if not config:
            raise ValueError("設定が存在しないか無効です。")

        connect_to_wifi(config.get('SSID'), config.get('PASSWORD'))

        while True:
            weather = get_weather()
            if weather:
                description, temperature = weather
                display_weather(description, temperature)
            time.sleep(UPDATE_INTERVAL)

    except (RuntimeError, ValueError) as e:
        print(f"エラー: {e}")
        print("プログラムを終了します...")
    finally:
        print("リソースを解放中...")
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)


if __name__ == "__main__":
    main()
