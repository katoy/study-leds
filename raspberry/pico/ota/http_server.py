#!/usr/bin/env python3
"""
OTA更新用の安定版HTTPサーバー
接続エラーを適切にハンドリングし、ログを整理したバージョン
"""

import http.server
import socketserver
import json
import os
import sys
import logging
from datetime import datetime

# ログ設定（エラーを抑制）
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class QuietOTAHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        from datetime import datetime
        try:
            if self.path == '/log':
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    msg = data.get('msg', '')
                except Exception:
                    msg = post_data.decode('utf-8')
                timestamp = datetime.now().strftime("%H:%M:%S")
                client_ip = self.client_address[0]
                print(f"[{timestamp}] 📝 [Pico LOG] {client_ip}: {msg}")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
                self.wfile.flush()
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")
    """接続エラーを静かに処理するOTAハンドラー"""

    def log_message(self, format, *args):
        """成功したリクエストのみログ出力"""
        if "200" in (format % args):  # 成功したリクエストのみ表示
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ✅ {self.address_string()} - {format % args}")

    def log_error(self, format, *args):
        """エラーログを抑制"""
        # Socket エラーは無視、その他のエラーのみ表示
        error_msg = format % args
        if "Socket is not connected" not in error_msg and "Broken pipe" not in error_msg:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ⚠️  Error: {error_msg}")

    def do_GET(self):
        client_ip = self.client_address[0]
        timestamp = datetime.now().strftime("%H:%M:%S")

        if self.path == '/versions.json':
            print(f"[{timestamp}] 🔎 [UPDATE CHECK] Pico ({client_ip}) is checking for updates.")
        elif self.path.endswith('.py'):
            print(f"[{timestamp}] ⬇️ [DOWNLOAD] Pico ({client_ip}) is downloading {self.path}.")

        try:
            if self.path == '/versions.json':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Connection', 'close')  # 接続を即座に閉じる
                self.end_headers()

                # versions.jsonファイルを読み込んで返す
                try:
                    with open('versions.json', 'r') as f:
                        content = f.read()
                    self.wfile.write(content.encode('utf-8'))
                except FileNotFoundError:
                    error_response = {
                        "error": "versions.json not found",
                        "version": "0.0.0",
                        "files": []
                    }
                    self.wfile.write(json.dumps(error_response).encode('utf-8'))
            else:
                # 通常のファイル配信
                path = self.translate_path(self.path)
                try:
                    f = open(path, 'rb')
                except OSError:
                    self.send_error(404, "File not found")
                    return

                self.send_response(200)
                self.send_header('Content-type', self.guess_type(path))
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs.st_size))
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Connection', 'close')
                self.end_headers()

                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()
        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            # 接続エラーは静かに処理
            pass
        except Exception as e:
            # その他のエラーのみログ出力
            logger.warning(f"Unexpected error: {e}")

class StableTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """安定したTCPサーバー（エラー抑制版）"""
    allow_reuse_address = True
    daemon_threads = True
    timeout = 10  # タイムアウトを短縮

    def handle_error(self, request, client_address):
        """接続エラーを静かに処理"""
        exc_type, exc_value, exc_traceback = sys.exc_info()

        # Socket関連のエラーは無視
        if isinstance(exc_value, (OSError, ConnectionResetError, BrokenPipeError)):
            if "Socket is not connected" in str(exc_value) or "Broken pipe" in str(exc_value):
                return  # 静かに無視

        # その他のエラーのみログ出力
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] ⚠️  Connection error from {client_address}: {exc_value}")

def main():
    PORT = 8080
    server_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(server_directory)

    print("🚀 安定版OTAサーバー起動中...")
    print(f"📁 配信ディレクトリ: {server_directory}")
    print(f"🌐 ポート: {PORT}")
    print("🔗 アクセスURL: http://localhost:8080/versions.json")
    print("📊 接続ログ（成功したリクエストのみ表示）:")
    print("⏹️  停止: Ctrl+C")
    print("-" * 50)

    # 現在のバージョンを表示
    try:
        with open('versions.json', 'r') as f:
            data = json.load(f)
        print(f"📦 配信中のバージョン: {data['version']}")
        print(f"📄 ファイル数: {len(data['files'])}")
        print("-" * 50)
    except:
        print("⚠️  versions.json が見つかりません")
        print("-" * 50)

    with StableTCPServer(("", PORT), QuietOTAHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 サーバー停止")
        except Exception as e:
            print(f"\n❌ サーバーエラー: {e}")

if __name__ == "__main__":
    main()