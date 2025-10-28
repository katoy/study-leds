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

    def check_and_update(self):
        """
        単発でアップデートチェックを行う（簡易実装）。
        サーバーの versions.json を取得してログ出力する（ダウンロードや置換は実装していない）。
        """
        msg = "[OTA] check_and_update: start"
        print(msg)
        # send_log は WiFi 接続後にのみ実行される仕様のため、ここでは print + send_log を行う
        try:
            self.log.send_log(msg)
        except Exception:
            # ログ送信失敗は致命的でないため無視
            pass

        try:
            url = self.server_url.rstrip('/') + '/versions.json'
            resp = None
            try:
                resp = self.urequests.get(url)
                status = getattr(resp, 'status_code', None)
                if status == 200 or status is None:
                    body = getattr(resp, 'text', None)
                    if body is None:
                        try:
                            body = resp.content
                        except Exception:
                            body = None
                    if body:
                        try:
                            data = self.ujson.loads(body)
                            msg = f"[OTA] remote version: {data.get('version')}"
                            print(msg)
                            try:
                                self.log.send_log(msg)
                            except Exception:
                                pass
                        except Exception as e_json:
                            msg = f"[OTA] JSON parse error: {e_json}"
                            print(msg)
                            try:
                                self.log.send_log(msg)
                            except Exception:
                                pass
                else:
                    msg = f"[OTA] Failed to fetch versions.json (status={status})"
                    print(msg)
                    try:
                        self.log.send_log(msg)
                    except Exception:
                        pass
            except Exception as e_req:
                msg = f"[OTA] request error: {e_req}"
                print(msg)
                try:
                    self.log.send_log(msg)
                except Exception:
                    pass
            finally:
                try:
                    if resp:
                        resp.close()
                except Exception:
                    pass
        except Exception as e:
            msg = f"[OTA] check_and_update exception: {e}"
            print(msg)
            try:
                self.log.send_log(msg)
            except Exception:
                pass

        msg = "[OTA] check_and_update: done"
        print(msg)
        try:
            self.log.send_log(msg)
        except Exception:
            pass
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
