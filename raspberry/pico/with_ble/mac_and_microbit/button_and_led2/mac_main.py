#!/usr/bin/env python3
import sys
import time
import select
from kaspersmicrobit import KaspersMicrobit

def main():
    # micro:bit を自動検出・接続
    with KaspersMicrobit.find_one_microbit(timeout=10) as mb:
        print(f"Connected to micro:bit @ {mb.address()}")

        stop_event = False
        last_text = None
        last_time = 0.0

        # UART 受信コールバック
        def on_uart(text: str):
            nonlocal stop_event, last_text, last_time
            text = text.strip()
            now = time.time()
            if text == last_text and (now - last_time) < 0.5:
                return
            last_text, last_time = text, now

            if text == "A":
                print("\n⟶ micro:bit Button A pressed")
            elif text == "B":
                print("\n⟶ micro:bit Button B pressed — Exiting…")
                stop_event = True
            else:
                print(f"\n⟶ Received UART: {text}")

        mb.uart.receive_string(on_uart)

        prompt = "[1] ON  [2] OFF  [q] Quit > "
        # 初回プロンプト表示
        sys.stdout.write(prompt)
        sys.stdout.flush()

        # ノンブロック入力ループ
        while not stop_event:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                choice = sys.stdin.readline().strip().lower()
                if choice == "1":
                    mb.uart.send_string("on\n")
                    print("✔ Sent UART: on")
                elif choice == "2":
                    mb.uart.send_string("off\n")
                    print("✔ Sent UART: off")
                elif choice == "q":
                    print("Exiting by user…")
                    break
                else:
                    print("Invalid selection.")
                # 入力処理後に改めてプロンプトを出す
                sys.stdout.write(prompt)
                sys.stdout.flush()

        print("Disconnecting…")

if __name__ == "__main__":
    main()
