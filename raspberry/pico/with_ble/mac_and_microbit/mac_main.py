# mac_main.py
import time
from kaspersmicrobit import KaspersMicrobit

def main():
    # with ブロックで自動 connect/discover/disconnect
    with KaspersMicrobit.find_one_microbit(timeout=5) as mb:
        print(f"Connected to micro:bit @ {mb.address()}")
        while True:
            choice = input("[1] ON  [2] OFF  [q] Quit > ").strip().lower()
            if choice == '1':
                mb.uart.send_string("on\n")   # 点灯コマンド送信
                print("Sent: on")
            elif choice == '2':
                mb.uart.send_string("off\n")  # 消灯コマンド送信
                print("Sent: off")
            elif choice == 'q':
                print("Exiting.")
                break
            else:
                print("Invalid selection.")
            time.sleep(0.5)

if __name__ == "__main__":
    main()
