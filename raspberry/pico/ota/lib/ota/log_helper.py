class LogHelper:
    def __init__(self, server_url=None):
        self.server_url = server_url

    def print_and_log(self, msg):
        try:
            print(msg)
        except Exception as e_print:
            self.send_log(f"[OTA] print failed: {e_print} (msg={msg})")
        self.send_log(msg)

    def send_log(self, msg):
        if not self.server_url:
            return
        try:
            import urequests
            import ujson
            url = self.server_url.rstrip('/') + '/log'
            payload = {'msg': msg}
            headers = {'Content-Type': 'application/json'}
            urequests.post(url, data=ujson.dumps(payload), headers=headers)
        except Exception as e:
            print(f"[OTA] (send_log failed) {e} url={self.server_url}")

    def append_debug(self, filename, text, max_bytes=16*1024):
        """
        ログファイルに時刻付きで追記し、max_bytes（デフォルト16KB）を超えたら古い行を切り詰める。
        """
        import time
        try:
            # 時刻付きで追記
            now = None
            try:
                now = time.time()
            except Exception:
                pass
            if now is not None:
                line = f"[{now}] {text}\n"
            else:
                line = text + '\n'

            # 既存サイズ確認
            try:
                import os
                size = os.stat(filename)[6]
            except Exception:
                size = 0

            # サイズ超過時は古い行を切り詰め
            if size > max_bytes:
                try:
                    with open(filename, 'r') as f:
                        lines = f.readlines()
                    # 直近半分だけ残す
                    keep = lines[-(len(lines)//2):] if len(lines) > 1 else lines
                    with open(filename, 'w') as f:
                        f.writelines(keep)
                except Exception:
                    pass

            with open(filename, 'a') as f:
                f.write(line)
        except Exception as e:
            print(f"[OTA] (append_debug failed) {e} file={filename}")
