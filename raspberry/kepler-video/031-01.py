"""
このプログラムは、OpenWeatherMap API から天気データを取得し、
SSD1306 OLED ディスプレイにリアルタイムで表示するためのものです。

主な機能:
1. Wi-Fi の接続情報と OpenWeatherMap の API キーを設定ファイルから読み込みます。
2. Wi-Fi に接続して、指定した間隔で天気データを取得します。
3. 取得した天気情報 (天気の説明、気温、湿度、気圧) を OLED ディスプレイに表示します。
4. 表示内容には日本時間 (UTC+9) が含まれます。
5. 長いテキストは自動で折り返してディスプレイに表示します。
6. プログラム終了時にリソースを適切に解放します。

使用方法:
1. `config.txt` に Wi-Fi の SSID、パスワード、API キーを記載してください。
2. SSD1306 OLED ディスプレイを I2C 接続 (GPIO 0: SDA, GPIO 1: SCL) で接続してください。
3. スクリプトを実行すると、天気情報がリアルタイムで表示されます。
"""

import network
import urequests
import time
import ntptime
import machine
import ssd1306

# 定数
UNITS = "metric"  # 温度単位 (摂氏)
CITY = 'tokyo'  # 都市名
LANG = 'en'  # 言語 ('ja' に設定すると日本語になります)
UPDATE_INTERVAL = 60  # 更新間隔 (秒)
CALL_API_INTERVAL = 60 * 5 

# I2C の設定
# SDA_PIN = machine.Pin(0)  # SDA ピン番号
# SCL_PIN = machine.Pin(1)  # SCL ピン番号
# i2c = machine.I2C(0, sda=SDA_PIN, scl=SCL_PIN, freq=400000)
# display = ssd1306.SSD1306_I2C(128, 64, i2c)

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
    if not ssid or not password:
        print("エラー: SSID またはパスワードが無効です。")
        machine.reset()

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

def sync_time():
    """NTP を使用してシステム時間を同期します。"""
    while True:
        try:
            ntptime.settime()
            print('時刻が正常に設定されました')
            break
        except OSError:
            print('時刻を設定中...')
            continue

def get_weather(api_key, city=CITY, units=UNITS, lang=LANG):
    """OpenWeatherMap API から天気データを取得します。"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}&lang={lang}"
    res = urequests.post(url)
    return res.json()

def get_japan_time():
    """UTC 時間を日本標準時 (UTC+9) に変換します。"""
    current_time = time.localtime()
    utc_to_jst = list(current_time)
    utc_to_jst[3] += 9

    if utc_to_jst[3] >= 24:
        utc_to_jst[3] -= 24
        utc_to_jst[2] += 1

        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (utc_to_jst[0] % 4 == 0 and utc_to_jst[0] % 100 != 0) or (utc_to_jst[0] % 400 == 0):
            days_in_month[1] = 29
        if utc_to_jst[2] > days_in_month[utc_to_jst[1] - 1]:
            utc_to_jst[2] = 1
            utc_to_jst[1] += 1

            if utc_to_jst[1] > 12:
                utc_to_jst[1] = 1
                utc_to_jst[0] += 1

    return tuple(utc_to_jst)

def draw_wrapped_text(display, text, x, y, max_width):
    """長いテキストを折り返して SSD1306 ディスプレイに表示します。"""
    lines = []
    words = text.split(' ')
    current_line = ""

    for word in words:
        test_line = current_line + ("" if current_line == "" else " ") + word
        width = len(test_line) * 8

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    line_height = 10
    for i, line in enumerate(lines):
        display.text(line, x, y + i * line_height)

def cleanup():
    """リソースを解放します。"""
    print("リソースを解放中...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)

def main():
    """メインプログラムループ。"""
    try:
        config = load_config()
        if not config:
            raise ValueError("設定が存在しないか無効です。")
        ip = connect_to_wifi(config.get('SSID'), config.get('PASSWORD'))
        print(f"デバイスが準備完了しました。IP: {ip}")
        sync_time()

        description = None
        temp_c  = None
        humidity  = None
        pressure = None
        while True:
            japan_time = get_japan_time()
            print(f"{japan_time[0]}-{japan_time[1]:02}-{japan_time[2]:02} "
                  f"{japan_time[3]:02}:{japan_time[4]:02}")
            
            if int(japan_time[4]) % CALL_API_INTERVAL == 0 or description is None:
                weather_data = get_weather(config['OPENWEATHER_API_KEY'])
                description = weather_data['weather'][0]['description']
                temp_c = weather_data['main']['temp']
                humidity = weather_data['main']['humidity']
                pressure = weather_data['main']['pressure']
            
                print(f"天気: {description}")
                print(f"気温: {temp_c} C")
                print(f"湿度: {humidity} %")
                print(f"気圧: {pressure} hPa")

            display.fill(0)
            display.text(
                f"{japan_time[0]}-{japan_time[1]:02}-{japan_time[2]:02} "
                f"{japan_time[3]:02}:{japan_time[4]:02}", 0, 0)
            display.text(f"{temp_c} C, {humidity} % ", 8, 15)
            display.text(f"{pressure} pHa ", 8, 30)
            draw_wrapped_text(display, description, x=8, y=45, max_width=128)
            display.show()

            time.sleep(UPDATE_INTERVAL)

    except (RuntimeError, ValueError) as e:
        print(f"エラー: {e}")
        print("プログラムを終了します...")
    finally:
        cleanup()

if __name__ == "__main__":
    main()
