import machine
import time
from buzzer_music import music

# 各音符データは、開始時間、音の高さ（ノート）、持続時間、楽器番号の順に並んでいます。
# 楽器番: 0 (Elec.Piano(Classic))

# https://onlinesequencer.net でメロディデータを作成できます。
# 1. onlinesequencer.netで再生したい音楽を作成または選択します。
# 2. 「Edit」ボタンをクリックし、Ctrl + Aで全ての音符を選択し、Ctrl + Cでコピーします。
# 3. コピーしたデータから、先頭の"Online Sequencer:数字:"と末尾の";:"を削除し、純粋な音符データのみを取得します。

# https://onlinesequencer.net/2474257
# song = "0 G4 3 0;3 G4 1 0;4 A4 4 0;8 G4 4 0;12 C5 4 0;16 B4 8 0;24 G4 3 0;27 G4 1 0;28 A4 4 0;32 G4 4 0;36 D5 4 0;40 C5 8 0;48 G4 3 0;51 G4 1 0;52 G5 4 0;56 E5 4 0;60 C5 4 0;64 B4 4 0;68 A4 4 0;72 F5 3 0;75 F5 1 0;76 E5 4 0;80 C5 4 0;84 D5 4 0;88 C5 8 0"

# ブザーを接続したGPIOピンの設定
buzzer_pin = 15
song = "0 C4 8 0;8 D4 8 0;16 E4 8 0;24 F4 8 0;32 G4 8 0"

# Initialize the music class with the song and set the buzzer pin
mySong = music(song, pins=[machine.Pin(buzzer_pin)])

# Play music using the music class.
try:
    while True:
        mySong.tick()  # 音楽の再生を進める
        time.sleep(0.05)  # 適切な間隔で tick を呼び出す
except KeyboardInterrupt:
    # Ctrl+C が押された場合の処理
    print("再生を停止します。")
    mySong.stop()  # 音楽の再生を停止
    # 必要に応じて、ブザーピンを無効化
    buzzer = machine.Pin(buzzer_pin, machine.Pin.OUT)
    buzzer.value(0)
    print("プログラムを終了します。")
