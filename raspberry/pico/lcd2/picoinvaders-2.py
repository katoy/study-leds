# See
#  https://www.youtube.com/watch?v=O5S1LC5TFiM
#  https://github.com/printnplay/Pico-MicroPython/blob/main/picoinvaders.py

"""
# プログラム概要
# Raspberry Pi Pico 用スペースインベーダー風ゲーム
#
# 機能:
# - SSD1306 OLED ディスプレイを利用して敵キャラクターやスコアを描画
# - ポテンショメータで操作可能なプレイヤーの移動
# - PWM を使用したスピーカー（パッシブブザー）からの効果音
# - UFO 出現やエイリアンのアニメーション描画
#
# 動作方法:
# - ポテンショメータを回してプレイヤーの移動位置を調整
# - 自動で発射されるレーザーでエイリアンを撃破
# - スコアと難易度はディスプレイに表示

# 配線方法:
# 1. SSD1306 OLED ディスプレイ (I2C 接続)
#    - SDA ピン: GP0
#    - SCL ピン: GP1
#    - VCC: 3.3V ピン
#    - GND: GND ピン
#
# 2. ポテンショメータ
#    - 中央端子: GP26 (ADC0)
#    - 一端: 3.3V ピン
#    - 他端: GND ピン
#
# 3. パッシブブザー（トランジスタ回路を使用）
#    - GPIO ピン: GP15
#    - 抵抗 (1kΩ): GP15 → トランジスタのベース端子
#    - トランジスタ (NPN, 例えば 2N2222)
#        - ベース: 抵抗を介して GP15 に接続
#        - エミッタ: GND に接続
#        - コレクタ: パッシブブザーの負極に接続
#    - パッシブブザーの正極: 3.3V ピンに接続
#
# 回路図:
#            3.3V ---- (正極) パッシブブザー (負極) ---- コレクタ(トランジスタ)
#                                |
#                                +---- ベース --- 抵抗 (1kΩ) --- GP15 (PWM)
#                                |
#                               エミッタ --- GND
#
# 注意事項:
# - SSD1306 の解像度は 128x64 ピクセルに設定
# - I2C 通信のピン番号や周波数は環境に応じて調整
# - パッシブブザーを直接 GPIO ピンに接続せず、トランジスタを介してください。
#
# See:
# https://www.youtube.com/watch?v=O5S1LC5TFiM
# https://github.com/printnplay/Pico-MicroPython/blob/main/picoinvaders.py
# https://docs.sunfounder.com/projects/kepler-kit/ja/latest/pyproject/py_pa_buz.html
#
# TODO:
# - エイリアンからの攻撃追加
# - シールド機能追加
# - 効果音の改良
"""

from machine import Pin, I2C, ADC, PWM
from ssd1306 import SSD1306_I2C
from time import sleep
import framebuf
import random

WIDTH  = 128 # oled display width
HEIGHT = 64  # oled display height
IS_LOWER = False

pot = ADC(26)
conversion_factor = 3.3 / (65535) # Conversion from Pin read to proper voltage
speaker = PWM(Pin(15))
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000) # Init I2C using I2C0 defaults, SCL=Pin(GP9), SDA=Pin(GP8), freq=400000
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)            # Init oled display

patterns = {}

aliens = []

class Alien(object):
    def __init__(self, type, x, y):
        self.visible = True
        self.type = type
        self.x = x
        self.y = y
        self.origx = x
        self.origy = y

def create_alien(type, x, y):
    return Alien(type, x, y)

def define_aliens(spritex, spritey, aliencountx, aliencounty, alienspacingx, alienspacingy):
    type = 'inv1a' # First row is type 1.
    for x in range(1, aliencountx + 1):
        for y in range(1, aliencounty + 1):
            aliens.append(
                create_alien(
                    type,
                    (120 - ((x * (spritex + alienspacingx)) - spritex)),
                    (y * (spritey + alienspacingy)) - spritey)
            )
        type ='inv2a' if type == 'inv1a' else 'inv1a'

def reset_aliens(visibility): # Used to reset aliens to starting position and, optionally, visibility
   for alien in aliens:
        alien.x = alien.origx
        alien.y = alien.origy
        if visibility:
            alien.visible = True

def cleanup():
    """ブザーを停止し、ディスプレイをクリアする"""
    speaker.duty_u16(0)    # ブザーを停止
    # oled.fill(0)         # ディスプレイをクリア
    # oled.text("Stopped", 0, 0)
    # oled.show()

def game_framebufs():
    if IS_LOWER == True:
        # smaller alien sprites. set spritex to 5 and spritey to 5
        inv1a = bytearray(b"\xd0xPx\xf0")
        inv1b = bytearray(b"\xf0xPx\xd0")
        inv2a = bytearray(b"\xe0P\xf8P\xe0")
        inv2b = bytearray(b"`\xd0x\xd0`")
        spritex = 5 # how big are your alien sprites?
        spritey = 5
        aliencountx = 4 # How many rows and columns of aliens
        aliencounty = 5
        alienspacingx = 5
        alienspacingy = 3
    else:
        # sprite definitions for Aliens. set spritex and spritey to 7
        inv1a = bytearray(b"~\xd8\x88\xf8\x88\xd8~")
        inv1b = bytearray(b"|\xda\xc8\xf8\xc8\xda|")
        inv2a = bytearray(b"\x88\\:\x1e:\\\x88")
        inv2b = bytearray(b"\x08\\\xba\x1e\xba\\\x08")
        spritex = 7 # how big are your alien sprites?
        spritey = 7
        aliencountx = 4 # How many rows and columns of aliens
        aliencounty = 4
        alienspacingx = 3
        alienspacingy = 3

    logo = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x01\xff\x80\x00\x07\xbd\xe0\x00\x00\x00\x00\x03\xe0\x00\x00\x00\x01\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x00\x00\x00\x00\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\xff\xfc\x07\xff\xe0\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\xff\xfc\x07\xff\xe0\x01\x08\x80\x00\x00\x01\xef\x00\x00\x00\x00\x00\x00\x07\xff\xe0\x01\xff\x80\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x008\xe0\x00\xf7\x00\x00\x07\xbd\xefx\x1e\x00\x02\xff\x00\x00\x18\xe0\x00\x00\x00\x00\x07\xbd\xefx\x1e\x00?\xff\x00\x00?\xe0\x00\x0c\x00\x00\x07\xbd\xefx\x1e\x00?\xd0\x00\x00\x1f\xc0\x08<\x00\x00\x07\xbd\xefx\x1e\x00<\x00\x00\x00\x0f\x80\x0c\xf0\x00\x00\x00\x00\x00\x00\x00\x00?\xff\x00\x00\x00\x00\x07\xc0\x00\x00\xf0=\xe0{\xc0\x00?\xff\x00\x00\x00\x00\x03\xc0\x00\x00\xf0=\xe0{\xc0\x00\x00\xbf\x00\x00\x00\x00\x00\xf0\x00\x00\xf0=\xe0{\xc0\x00\x00\x00\x00\x00\x00\x00\x00<\x00\x00\xf0=\xe0{\xc0\x00\x00`\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xc0\x07\xff\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00\x7f\xfe\x07\xff\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00\x1e\xfe\x07\xff\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00\x18\x1e\x00\x00\x00\x00\x00\x00\x00\xf0=\xefx\x00\x00\x00?\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xfe\x00\x00\x00\x01\xff\x80\x00\x00=\xefx\x00\x00\x00\x7f\x80\x00\x00\x00\x01\xff\x80\x00\x00=\xefx\x00\x00\x00@\x00\x00\x00\x00\x00\x10\x80\x00\x00=\xefx\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x80\x00\x00=\xefx\x00\x00?\xff\x00\x01\xff\x80\x00\x10\x80\x00\x00\x00\x00\x00\x00\x00?\xff\x00\x03\xff\xc0\x00\x10\x80\x00\xf0=\xefx\x00\x00?\xff\x00\x07\xff\xe0\x00\x1f\x80\x00\xf0=\xefx\x00\x008\x07\x00\x07\x00\xe0\x00\x0f\x00\x00\xf0=\xefx\x00\x000'\x00\x06\x00\xe0\x00\x00\x00\x00\xf0=\xefx\x00\x00?\xff\x00\x07\xe7\xe0\x01\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x1f\xfe\x00\x03\xe3\xc0\x01\xfc\x00\x00\xf0=\xe0{\xc0\x00\x0f\xfc\x00\x01\xe3\x80\x00\x04\x00\x00\xf0=\xe0{\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\xf0=\xe0{\xc0\x00\x00\x7f\xfe\x00\x00\x00\x01\xfc\x00\x00\xf0=\xe0{\xc0\x00\x00\x7f\xfe\x00\x00\x00\x01\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xfe\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xefx\x1e\x00\x00q\xce\x01\xff\x80\x00\x00\x00\x00\x07\xbd\xefx\x1e\x00\x00`\xc6\x03\xff\xc0\x01\xff\x80\x00\x07\xbd\xefx\x1e\x00\x00p\x8e\x07\xff\xe0\x01\xff\x80\x00\x07\xbd\xefx\x1e\x00\x00\x00\x00\x07\x00\xe0\x00\x10\x80\x00\x00\x00\x00\x00\x00\x00\xff\xfc\x00\x06\x04\xe0\x00\x10\x80\x00\x00\x01\xef\x00\x00\x00\xff\xfc\x00\x07\xff\xe0\x00\x10\x80\x00\x00\x01\xef\x00\x00\x00\xff\xfc\x00\x03\xff\xc0\x00\x10\x80\x00\x00\x01\xef\x00\x00\x00\x03\x9c\x00\x01\xff\x80\x00\x1f\x80\x00\x00\x01\xef\x00\x00\x00\t\x9c\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x00\xff\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\xfe\xf8\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\xfep\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07\xbd\xe0\x00\x00\x00\x00\x1cx\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00<\xfc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|\xfe\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00q\xce\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x7f\xde\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00?\x9c\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x18\x00\x00\x00")
    ship = bytearray(b" p\xf8l>//>l\xf8p ")
    ufo = bytearray(b"\x0c\x00>\x80\x1d\x80\r\xe0\x1d\xc0\x15\x80>\x80\x0c\x00")

    num0 = bytearray(b"\x7f\x80\xff\xc0\x80@\x80@\xff\xc0\x7f\x80")
    num1 = bytearray(b"\x00\x00\x00\x80\x00\x80\xff\xc0\xff\xc0\x00\x00")
    num2 = bytearray(b"\xe1\x80\xf1\xc0\x98@\x8c@\x87\xc0\x83\x80")
    num3 = bytearray(b"@\x80\xc0\xc0\x84@\x84@\xff\xc0{\x80")
    num4 = bytearray(b"0\x00<\x00/\x00#\x80\xff\xc0\xff\xc0")
    num5 = bytearray(b"O\xc0\xcf\xc0\x84@\x84@\xfc@x@")
    num6 = bytearray(b"\x7f\x80\xff\xc0\x84@\x84@\xfc\xc0x\x80")
    num7 = bytearray(b"\x00@\xe0@\xfc@\x1f@\x03\xc0\x00\xc0")
    num8 = bytearray(b"{\x80\xff\xc0\x84@\x84@\xff\xc0{\x80")
    num9 = bytearray(b"G\x80\xcf\xc0\x88@\x88@\xff\xc0\x7f\x80")

    # Load images into framebuffer
    inv1aBuff = framebuf.FrameBuffer(inv1a, spritex, spritey, framebuf.MONO_HLSB)
    inv1bBuff = framebuf.FrameBuffer(inv1b, spritex, spritey, framebuf.MONO_HLSB)
    inv2aBuff = framebuf.FrameBuffer(inv2a, spritex, spritey, framebuf.MONO_HLSB)
    inv2bBuff = framebuf.FrameBuffer(inv2b, spritex, spritey, framebuf.MONO_HLSB)

    ufoBuff = framebuf.FrameBuffer(ufo, 12, 8, framebuf.MONO_HLSB)
    logoBuff = framebuf.FrameBuffer(logo, 128, 64, framebuf.MONO_HLSB)

    # Dictionary for lookup of digits for score, level, possibly lives
    numbersBuff = {
        '0': framebuf.FrameBuffer(num0, 10, 6, framebuf.MONO_HLSB),
        '1': framebuf.FrameBuffer(num1, 10, 6, framebuf.MONO_HLSB),
        '2': framebuf.FrameBuffer(num2, 10, 6, framebuf.MONO_HLSB),
        '3': framebuf.FrameBuffer(num3, 10, 6, framebuf.MONO_HLSB),
        '4': framebuf.FrameBuffer(num4, 10, 6, framebuf.MONO_HLSB),
        '5': framebuf.FrameBuffer(num5, 10, 6, framebuf.MONO_HLSB),
        '6': framebuf.FrameBuffer(num6, 10, 6, framebuf.MONO_HLSB),
        '7': framebuf.FrameBuffer(num7, 10, 6, framebuf.MONO_HLSB),
        '8': framebuf.FrameBuffer(num8, 10, 6, framebuf.MONO_HLSB),
        '9': framebuf.FrameBuffer(num9, 10, 6, framebuf.MONO_HLSB)}

    shipBuff = framebuf.FrameBuffer(ship, 8, 12, framebuf.MONO_HLSB)

    return {
        'inv1a': inv1aBuff,
        'inv1b': inv1bBuff,
        'inv2a': inv2aBuff,
        'inv2b': inv2bBuff,

        'ufo':   ufoBuff,
        'logo':  logoBuff,
        'nums':  numbersBuff,
        'ship':  shipBuff,
    }

def sound_ufo(show_flag, soundfreq):
    if show_flag:
        # Toggle between 1100 and 2000
        soundfreq = 2000 if soundfreq == 1100 else 1100
    else:
        # Cycle through [180, 160, 140, 120]
        next_freqs = {180: 160, 160: 140, 140: 120, 120: 180}
        soundfreq = next_freqs.get(soundfreq, 180)  # Default to 180 if not in cycle

    speaker.freq(soundfreq)
    speaker.duty_u16(2000)

    return soundfreq

def shot_delete(soundfreq):
    speaker.duty_u16(0)
    soundfreq = 1000
    speaker.freq(soundfreq)
    speaker.duty_u16(2000)
    return soundfreq


def show_score(score, difficulty, patterns):
    numcount = 0 # keeps track of the number of times through the loop!
    for c in str(score):
        oled.blit(patterns['nums'][c], 1, ((numcount * 7) + 2)) # Display the score, 1 digit at a time
        numcount = numcount + 1

    numcount = 0
    for c in str(difficulty):
        oled.blit(patterns['nums'][c], 1, 48 + ((numcount * 7) + 2)) # Display the level, 1 digit at a time
        numcount = numcount + 1

    oled.show()

def show_logo(logo):
    # Clear the oled display in case it has junk on it.
    oled.fill(0)
    oled.blit(logo, 0, 0)

    # Finally update the oled display so the image & text is displayed
    oled.show()
    sleep(2)

def handle_ufo_appearance(showufo, ufoy, shotx, soundfreq):
    if showufo:
        soundfreq = sound_ufo(True, soundfreq)
    if shotx > 36 and not showufo:
        speaker.duty_u16(0)
    if showufo:
        ufoy += 1
        if ufoy > 64:
            showufo = False
    else:
        ufoChance = random.randrange(1, 350)
        if ufoChance == 123:
            showufo = True
            ufoy = 0
    return showufo, ufoy, soundfreq

def show_ship_shot_score(showufo, shippos, shotx, shoty, score, patterns, difficulty, soundfreq):
    oled.blit(patterns['ship'], 18, int(shippos)) # draw the ship
    oled.line(shotx, shoty, shotx - 4, shoty, 1)  # draw the laser
    show_score(score, difficulty, patterns)       # draw score
    if shotx == 32 and showufo == False:
        soundfreq = shot_delete(soundfreq)
    return soundfreq

def handle_alian_and_shot(aliens, shotx, shoty, score, foundVisible, showufo, ufoy, patterns, shippos):
    for c in aliens:
        if shotx >= c.x and c.visible == True: # Collision detection for aliens with the shots
            if shotx - 4 <= c.x + 8:
                if shoty > c.y:
                    if shoty <= c.y + 7: # You hit an alien!
                        c.visible = False
                        score += 10
                        shotx = 32
                        shoty = int(shippos) + 6
        if c.visible == True:
            foundVisible = True
            oled.blit(patterns[c.type], c.x, c.y)

        if showufo:
            oled.blit(patterns['ufo'], 120, ufoy)

    return shotx, shoty, score, foundVisible

def handle_ufo_and_shot(showufo, ufoy, shotx, shoty, score, shippos):
    if showufo:
        if shotx > 120:
            if shoty >= ufoy:
                if shoty < ufoy + 12:
                    score += 50
                    showufo = False
                    ufoy = 0
                    shotx = 20
                    shoty = int(shippos) + 6
    return showufo, ufoy, shotx, shoty, score

def handle_shot(shotx, shoty, shippos):
    if shotx > 130:
        shotx = 32
        shoty = int(shippos) + 6
    return shotx, shoty

def handle_difficulty(difficulty, foundVisible):
    if not foundVisible: # You finish the level! Increase the difficulty and reset the aliens
        if difficulty < 10:
            difficulty += 1
        reset_aliens(True)
    return difficulty

def hande_aliens(loopCount, addy, soundfreq, difficulty, showufo):
    loopCount += 1
    if loopCount > 16 - difficulty:
        if showufo == False:
            soundfreq = sound_ufo(False, soundfreq)

        dropdown = False
        loopCount = 0
        for c in aliens:
            if c.visible == True: # switch between sprites to animate aliens
                if c.type == 'inv1a': c.type = 'inv1b'
                elif c.type == 'inv1b': c.type = 'inv1a'
                elif c.type == 'inv2a': c.type = 'inv2b'
                elif c.type == 'inv2b': c.type = 'inv2a'
                if c.y + addy > 56 or c.y + addy < 0: # are any of the visible invaders at the edge of the screen?
                    if c.x - 3 < 20: # If they're at the bottom, reset their position
                        reset_aliens(False)
                        dropdown = False
                    dropdown = True
        if dropdown == True: # move the aliens down if any of the visible ones hit the screen edge
            addy = addy * -1
            for c in aliens:
                c.x = c.x - 3
        else:
            for c in aliens:
                c.y = c.y + addy
    return loopCount, addy, soundfreq

def main():
    soundfreq = 160
    patterns = game_framebufs()

    spritex = 5 # how big are your alien sprites?
    spritey = 5
    aliencountx = 4 # How many rows and columns of aliens
    aliencounty = 5
    alienspacingx = 5
    alienspacingy = 3
    if not IS_LOWER:
        spritex += 2 # how big are your alien sprites?
        spritey += 2
        aliencounty -= 1
        alienspacingx -= 2

    show_logo(patterns['logo'])

    define_aliens(spritex, spritey, aliencountx, aliencounty, alienspacingx, alienspacingy)

    addy = 3 # pixels of movement per turn on aliens
    shotx = 0
    shoty = 999
    loopCount = 0
    score = 0
    difficulty = 1
    showufo = False
    ufoy = 0
    ufoCount = 0

    while True:
        oled.fill(0)
        showufo, ufoy, soundfreq = handle_ufo_appearance(showufo, ufoy, shotx, soundfreq)
        loopCount, addy, soundfreq = hande_aliens(
            loopCount, addy, soundfreq, difficulty, showufo)

        shippos = (pot.read_u16() * conversion_factor) # Read potentiometer to get ship position
        shippos = (64 - ((52 / 3.3) * shippos) - 12)
        shotx = shotx + 2
        foundVisible = False # By default, assume all the aliens are dead

        showufo, ufoy, shotx, shoty, score = handle_ufo_and_shot(
            showufo, ufoy, shotx, shoty, score, shippos)
        shotx, shoty, score, foundVisible = handle_alian_and_shot(
            aliens, shotx, shoty, score, foundVisible, showufo, ufoy, patterns, shippos)
        shotx, shoty = handle_shot(
            shotx, shoty, shippos)
        difficulty = handle_difficulty(
            difficulty, foundVisible)
        soundfreq = show_ship_shot_score(
            showufo, shippos, shotx, shoty, score, patterns, difficulty, soundfreq)
        sleep(0.001)

try:
    main()
except KeyboardInterrupt:
    cleanup()  # Ctrl-C が押されたらリソースを解放
    print('プログラムが停止しました。')
