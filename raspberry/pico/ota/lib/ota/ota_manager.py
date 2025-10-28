from .log_helper import LogHelper


class OTAManager:
    def __init__(self, wifi_ssid, wifi_password, server_url,
                 check_interval=60, version_file="version.txt", auto_reboot=True,
                 network_mod=None, urequests_mod=None, ujson_mod=None, machine_mod=None,
                 time_mod=None, gc_mod=None, os_mod=None):
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.server_url = server_url
        self.check_interval = check_interval
        self.version_file = version_file
        self.auto_reboot = auto_reboot

        # allow dependency injection for testing/runtime variations
        self.network = network_mod if network_mod else __import__('network')
        self.urequests = urequests_mod if urequests_mod else __import__('urequests')
        self.ujson = ujson_mod if ujson_mod else __import__('ujson')
        self.machine = machine_mod if machine_mod else __import__('machine')
        self.time = time_mod if time_mod else __import__('time')
        self.gc = gc_mod if gc_mod else __import__('gc')
        self.os = os_mod if os_mod else __import__('os')

        # --- WiFiインターフェース強制リセット ---
        try:
            wlan = self.network.WLAN(self.network.STA_IF)
            wlan.active(False)
            self.time.sleep(1)
            wlan.active(True)
        except Exception:
            pass
        self.wlan = self.network.WLAN(self.network.STA_IF)
        self.last_check_time = 0
        self.wifi_connected = False
        self.log = LogHelper(server_url)

    def connect_wifi(self):
        """
        WiFi接続を確立する。既に接続済みなら何もしない。
        ログはファイルに追記する（WiFi未接続時にHTTP送信を試行しないため）。
        """
        # self.wifi_connected チェックは不要。常に実際のインターフェース状態で判定する。

        # 既に内部状態として接続されていないか、インターフェースが接続済みかを確認
        try:
            if getattr(self.wlan, 'isconnected', lambda: False)():
                self.wifi_connected = True
                msg = f"[OTA] WiFi already connected: {self.wlan.ifconfig()}"
                self.log.append_debug("wifi.log", msg)
                return
        except Exception:
            # 不要な例外で停止しない
            pass

        # ファイルにログを残す（ネットワーク未接続でも書ける）
        self.log.append_debug("wifi.log", "[OTA] Connecting WiFi...")

        # 有効化と接続要求
        try:
            self.wlan.active(True)
        except Exception:
            # 一部プラットフォームでは active が例外を投げる可能性がある
            pass

        try:
            self.wlan.connect(self.wifi_ssid, self.wifi_password)
        except Exception as e_conn:
            self.log.append_debug("wifi.log", f"[OTA] wlan.connect raised: {e_conn}")

        # 接続待ち: 長めに待つ（例: 30秒間、0.5s間隔）
        attempts = 20
        delay = 0.5
        for i in range(attempts):
            try:
                if self.wlan.isconnected():
                    msg = f"[OTA] WiFi connected: {self.wlan.ifconfig()} ({i+1}/{attempts})"
                    self.log.append_debug("wifi.log", msg)
                    return
            except Exception:
                pass
            try:
                self.time.sleep(delay)
            except Exception:
                pass
        # 全試行失敗時にも試行回数を記録
        self.log.append_debug("wifi.log", f"[OTA] WiFi connection failed! ({attempts}/{attempts})")

        # 接続失敗時はインターフェースをリセットしてログを残す
        self.log.append_debug("wifi.log", "[OTA] WiFi connection failed!")
        try:
            # いったん off/on して状態をクリア（失敗しても継続）
            self.wlan.active(False)
            try:
                self.time.sleep(1)
            except Exception:
                pass
            self.wlan.active(True)
        except Exception:
            pass

            # 自動リセット（MicroPython/Pico W環境想定）
            try:
                self.machine.reset()
            except Exception:
                pass
            # 念のため例外もraise（boot.py等の上位で再起動ロジックがある場合）
            raise RuntimeError("WiFi接続に失敗しました")

    def get_current_version(self):
        """ローカルのバージョンファイルから現在のバージョンを読み込む"""
        try:
            with open(self.version_file, 'r') as f:
                return f.read().strip()
        except Exception:
            return "0.0.0"

    def set_current_version(self, version):
        """ローカルのバージョンファイルに現在のバージョンを書き込む"""
        with open(self.version_file, 'w') as f:
            f.write(version)

    def _ensure_dirs(self, file_path):
        if '/' in file_path:
            parts = file_path.split('/')[:-1]
            path = ''
            for i, part in enumerate(parts):
                path = '/'.join(parts[:i+1])
                try:
                    self.os.mkdir(path)
                except OSError as e:
                    if e.args[0] != 17: # EEXIST
                        raise

    def download_file(self, url, dest_path):
        """ファイルをダウンロードして指定されたパスに保存する"""
        self.gc.collect()
        self._ensure_dirs(dest_path)
        try:
            resp = self.urequests.get(url)
            if resp.status_code == 200:
                # メモリ節約のため、チャンクで書き込む
                buf = bytearray(256)
                with open(dest_path, 'wb') as f:
                    while True:
                        size = resp.raw.readinto(buf)
                        if size == 0:
                            break
                        f.write(buf, size)
                return True
            else:
                print(f"[OTA] ERROR: Download failed (status={resp.status_code}) url={url} dest={dest_path}")
                self.log.send_log(f"[OTA] ERROR: Download failed (status={resp.status_code}) url={url} dest={dest_path}")
                return False
        except Exception as e:
            print(f"[OTA] EXCEPTION: Download failed url={url} dest={dest_path} error={e}")
            self.log.send_log(f"[OTA] EXCEPTION: Download failed url={url} dest={dest_path} error={e}")
            return False
        finally:
            if 'resp' in locals() and resp:
                resp.close()

    def check_and_update(self):
        """
        サーバーと通信してOTAアップデートを実行する。
        """
        self.gc.collect()
        msg = "[OTA] check_and_update: start"
        print(msg)
        self.log.send_log(msg)

        current_version = self.get_current_version()
        msg = f"[OTA] Current version: {current_version}"
        print(msg)
        self.log.send_log(msg)

        try:
            url = self.server_url.rstrip('/') + '/versions.json'
            resp = self.urequests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                remote_version = data.get('version')
                msg = f"[OTA] Remote version: {remote_version}"
                print(msg)
                self.log.send_log(msg)

                if remote_version and remote_version != current_version:
                    msg = "[OTA] New version found, starting update..."
                    print(msg)
                    self.log.send_log(msg)

                    files_to_update = data.get('files', [])
                    for file_info in files_to_update:
                        file_url = file_info['url']
                        dest_path = file_info['name']
                        msg = f"[OTA] Downloading {file_url} to {dest_path}"
                        print(msg)
                        self.log.send_log(msg)
                        self.gc.collect()
                        if self.download_file(file_url, dest_path):
                            msg = f"[OTA] Downloaded {dest_path}"
                            print(msg)
                            self.log.send_log(msg)
                        else:
                            msg = f"[OTA] Failed to download {dest_path}"
                            print(msg)
                            self.log.send_log(msg)
                            # エラー処理: アップデートを中止
                            return False

                    self.set_current_version(remote_version)
                    msg = f"[OTA] Update complete. New version: {remote_version}"
                    print(msg)
                    self.log.send_log(msg)

                    if self.auto_reboot:
                        msg = "[OTA] Rebooting..."
                        print(msg)
                        self.log.send_log(msg)
                        self.machine.reset()
            else:
                msg = f"[OTA] Failed to fetch versions.json (status={resp.status_code})"
                print(msg)
                self.log.send_log(msg)
        except Exception as e:
            msg = f"[OTA] check_and_update exception: {e}"
            print(msg)
            self.log.send_log(msg)
        finally:
            if 'resp' in locals() and resp:
                resp.close()

        msg = "[OTA] check_and_update: done"
        print(msg)
        self.log.send_log(msg)
        return False

    def periodic_check(self):
        """定期チェック。最後のチェック時間から check_interval 秒が経過していれば check_and_update を呼ぶ。"""
        try:
            now = int(self.time.time())
        except Exception:
            try:
                now = int(self.time.ticks_ms() / 1000)
            except Exception:
                now = 0

        if self.last_check_time == 0:
            self.last_check_time = now
            return

        if now - self.last_check_time >= self.check_interval:
            msg = "[OTA] periodic_check: triggering check"
            print(msg)
            try:
                self.log.send_log(msg)
            except Exception:
                pass
            self.last_check_time = now
            try:
                self.check_and_update()
            except Exception as e:
                msg = f"[OTA] periodic_check failed: {e}"
                print(msg)
                try:
                    self.log.send_log(msg)
                except Exception:
                    pass