from .ota_manager import OTAManager
from machine import Pin, Timer

class OTAEnabledApp:
    """
    OTA機能を簡単に組み込むためのベースクラス
    """
    def __init__(self, app_name, version, wifi_ssid=None, wifi_password=None, server_url=None):
        self.app_name = app_name
        self.version = version

        # config.pyから設定を読み込み
        try:
            from config import WIFI_SSID, WIFI_PASSWORD, UPDATE_SERVER_URL
            wifi_ssid = wifi_ssid or WIFI_SSID
            wifi_password = wifi_password or WIFI_PASSWORD
            server_url = server_url or UPDATE_SERVER_URL
        except ImportError:
            try:
                from config import WIFI_SSID, WIFI_PASSWORD, UPDATE_SERVER_IP
                wifi_ssid = wifi_ssid or WIFI_SSID
                wifi_password = wifi_password or WIFI_PASSWORD
                server_url = server_url or f"http://{UPDATE_SERVER_IP}:8080"
            except ImportError:
                pass

        # デフォルト設定
        if not all([wifi_ssid, wifi_password, server_url]):
            print("[OTA] Warning: WiFi/Server settings not configured")
            wifi_ssid = wifi_ssid or "your_wifi_name"
            wifi_password = wifi_password or "your_wifi_password"
            server_url = server_url or "http://192.168.0.104:8080"

        self.ota = OTAManager(wifi_ssid, wifi_password, server_url)
        self.running = False

    def setup(self):
        """アプリケーションのセットアップ（オーバーライド必須）"""
        raise NotImplementedError()

    def run(self):
        d_led = Pin('LED', Pin.OUT)
        d_led.on()
        """アプリケーションのメインループ"""
        self.running = True
        self.ota.connect_wifi()

        # アプリケーションの現在のバージョンを記録
        current_local_version = self.ota.get_current_version()
        if self.version != current_local_version:
            self.ota.set_current_version(self.version)

        self.ota.check_and_update()
        self.setup()
        while self.running:
            self.loop()
            self.ota.periodic_check()

    def loop(self):
        """アプリケーションのループ処理（オーバーライド必須）"""
        raise NotImplementedError()

    def stop(self):
        self.running = False

    def send_log(self, msg):
        self.ota.send_log(msg)
