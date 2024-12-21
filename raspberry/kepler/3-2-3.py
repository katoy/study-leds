"""
Raspberry Pi Picoでパッシブブザーを使用してメロディを演奏するスクリプト

必要なハードウェア:
- Raspberry Pi Pico
- パッシブブザー
- S8050 NPNトランジスタ
- 1kΩ抵抗
- ブレッドボードとジャンパーワイヤー

配線方法:
1. Raspberry Pi PicoのGP15ピンを1kΩ抵抗を介してトランジスタのベース（B）に接続
2. トランジスタのエミッタ（E）をGNDに接続
3. トランジスタのコレクタ（C）をブザーの負極（短いピン）に接続
4. ブザーの正極（長いピン）を3.3V電源に接続

注: 配線方法の詳細は、SunFounderのKepler Kitドキュメントを参照してください。
URL: https://docs.sunfounder.com/projects/kepler-kit/ja/latest/pyproject/py_pa_buz.html
"""

import machine
import time
from buzzer_music import music

# ブザーを接続したGPIOピンの設定
BUSZZER_PIN = 15

# 演奏する楽曲データ
# 各音符は、開始時間、音の高さ（ノート）、持続時間、楽器番号の順に指定
# 楽器番号: 0 (エレクトリックピアノ（クラシック）)
# https://onlinesequencer.net でメロディデータを作成できます。
# 1. onlinesequencer.netで再生したい音楽を作成または選択します。
# 2. 「Edit」ボタンをクリックし、Ctrl + Aで全ての音符を選択し、Ctrl + Cでコピーします。
# 3. コピーしたデータから、先頭の"Online Sequencer:数字:"と末尾の";:"を削除し、純粋な音符データのみを取得します。

# See https://onlinesequencer.net/2474257
MY_SONG = (
    "0 G4 3 0;3 G4 1 0;4 A4 4 0;8 G4 4 0;"
    "12 C5 4 0;16 B4 8 0;24 G4 3 0;27 G4 1 0;"
    "28 A4 4 0;32 G4 4 0;36 D5 4 0;40 C5 8 0;"
    "48 G4 3 0;51 G4 1 0;52 G5 4 0;56 E5 4 0;"
    "60 C5 4 0;64 B4 4 0;68 A4 4 0;72 F5 3 0;"
    "75 F5 1 0;76 E5 4 0;80 C5 4 0;84 D5 4 0;"
    "88 C5 8 0"
)

# ジングルベル
MY_SONG = (
    "0 A5 1 0;4 A5 1 0;8 A5 1 0;16 A5 1 0;20 A5 1 0;24 A5 1 0;"
    "31 A5 1 0;32 A5 1 0;36 C6 1 0;40 F5 1 0;48 A5 1 0;46 G5 1 0;"
    "64 A#5 1 0;68 A#5 1 0;72 A#5 1 0;79 A#5 1 0;80 A#5 1 0;84 A5 1 0;"
    "88 A5 1 0;92 A5 1 0;94 A5 1 0;96 A5 1 0;100 G5 1 0;104 G5 1 0;"
    "108 A5 1 0;112 G5 1 0;120 C6 1 0;128 A5 1 0;132 A5 1 0;136 A5 1 0;"
    "144 A5 1 0;148 A5 1 0;152 A5 1 0;159 A5 1 0;160 A5 1 0;164 C6 1 0;"
    "168 F5 1 0;176 A5 1 0;174 G5 1 0;192 A#5 1 0;196 A#5 1 0;200 A#5 1 0;"
    "207 A#5 1 0;208 A#5 1 0;212 A5 1 0;216 A5 1 0;220 A5 1 0;222 A5 1 0;"
    "224 C6 1 0;232 A#5 1 0;236 G5 1 0;240 F5 1 0"
)

def main():
    # 楽曲データを使用してmusicクラスを初期化
    my_song = music(MY_SONG, pins=[machine.Pin(BUSZZER_PIN)])

    try:
        while True:
            my_song.tick()  # 音楽の再生を進行
            time.sleep(0.05)  # 適切な間隔で tick を呼び出す
    except KeyboardInterrupt:
        # Ctrl+C が押された場合の処理
        print("再生を停止します。")
        my_song.stop()  # 音楽の再生を停止
        # ブザーピンを無効化
        buzzer.deinit()
        print("プログラムを終了します。")

if __name__ == "__main__":
    main()
