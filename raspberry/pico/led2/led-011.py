import rp2
from machine import Pin
import time

CLOCK_FREQ = 2_000_000  # 2MHz

# 定数定義
DELAY_TRIGGER = 2000000   # trigger_sm 用：1秒遅延 (2MHzなら約2000000サイクル)
DELAY_BLINK   = 200000    # blink_sm 用：0.1秒遅延 (2MHzなら約200000サイクル)

# trigger_sm: FIFO から delay 値 (DELAY_TRIGGER) を取得し、delay ループ終了後に irq(1, 0) を実行する
@rp2.asm_pio(autopull=True, pull_thresh=32)
def trigger():
    wrap_target()
    pull()                # FIFO から 32bit 値（delay 値）を取得
    mov(x, osr)           # x にロード
    label("delay")
    jmp(x_dec, "delay")   # x が 0 になるまで 1サイクルずつデクリメント（約1秒遅延）
    irq(1, 0)             # IRQ0 をセットして blink_sm をトリガ
    wrap()

# blink_sm: trigger_sm からの IRQ を待機し、IRQ 受信後に FIFO の delay 値 (DELAY_BLINK) を取得して
# LED を 0.1 秒間 ON にし、その後 OFF にする
@rp2.asm_pio(sideset_init=rp2.PIO.OUT_LOW, autopull=True, pull_thresh=32)
def blink():
    wrap_target()
    wait(1, irq, 0)       # trigger_sm からの IRQ0 を待機
    set(pins, 1) .side(1)  # LED を ON にする
    pull()                # FIFO から 32bit 値（blink delay）を取得
    mov(x, osr)
    label("blink_delay")
    jmp(x_dec, "blink_delay")  # x が 0 になるまでループ（約0.1秒の遅延）
    set(pins, 0) .side(0)  # LED を OFF にする
    wrap()

# StateMachine の生成
trigger_sm = rp2.StateMachine(1, trigger, freq=CLOCK_FREQ)
blink_sm   = rp2.StateMachine(0, blink, freq=CLOCK_FREQ, sideset_base=Pin(15))

trigger_sm.active(1)
blink_sm.active(1)

# 初期投入: trigger_sm に 1秒遅延用 DELAY_TRIGGER、blink_sm に 0.1秒遅延用 DELAY_BLINK を投入
trigger_sm.put(DELAY_TRIGGER)
blink_sm.put(DELAY_BLINK)

# CPU 側のメインループで、1 秒ごとに各 StateMachine の FIFO に再供給する
try:
    while True:
        time.sleep(1)  # 1秒待機
        trigger_sm.put(DELAY_TRIGGER)
        blink_sm.put(DELAY_BLINK)
except KeyboardInterrupt:
    trigger_sm.active(0)
    blink_sm.active(0)
    Pin(15, Pin.OUT).value(0)
