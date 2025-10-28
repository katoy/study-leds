
# main.py を例外ハンドリング付きで起動し、失敗時はエラー出力＋自動リセット（3回までリトライ）
import machine
import time
import sys

def safe_run_main():
    for _ in range(3):
        try:
            import main
            break
        except Exception as e:
            print("main.py failed:", e)
            # エラー内容をファイル保存（失敗しても無視）
            try:
                with open('boot_error.log', 'w') as f:
                    f.write(str(e))
            except Exception:
                pass
            time.sleep(2)  # 少し待ってから自動リセット
            machine.reset()
        max_retry = 3
        for i in range(max_retry):
            try:
                import main
                break
            except Exception as e:
                print("main.py failed:", e)
                # エラー内容をファイル保存（失敗しても無視）
                try:
                    with open('boot_error.log', 'w') as f:
                        f.write(str(e))
                except Exception:
                    pass
                if i < max_retry - 1:
                    time.sleep(2)  # 少し待ってから自動リセット
                    machine.reset()
                else:
                    print("main.py failed too many times. Stopping auto-reboot loop.")
                    # 必要ならここでLED点滅や他の通知処理も可

safe_run_main()
