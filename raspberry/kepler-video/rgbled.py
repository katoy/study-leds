from machine import Pin, PWM

class RGBLED:
    # 色の辞書（クラス変数として定義）
    COLORS = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'yellow': (255, 255, 0),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203),
        'lime': (0, 255, 128),
        'brown': (139, 69, 19),
        'gray': (128, 128, 128),
        'lightgray': (192, 192, 192),
        'darkgray': (64, 64, 64),
        'white': (255, 255, 255),
        'off': (0, 0, 0)
    }

    # 大文字・小文字、アンダースコアを無視するための変換辞書
    NORMALIZED_COLORS = {key.replace("_", "").lower(): key for key in COLORS}

    def __init__(self, r: int, g: int, b: int):
        """RGB LED の PWM ピンを初期化"""
        self.redLED = PWM(Pin(r))
        self.greenLED = PWM(Pin(g))
        self.blueLED = PWM(Pin(b))

        # PWM 周波数を 1kHz に設定し、初期状態は消灯
        for led in (self.redLED, self.greenLED, self.blueLED):
            led.freq(1000)
            led.duty_u16(0)

    def set_color(self, color: str):
        """指定した色に LED を変更（大文字・小文字、アンダースコアの有無を無視）"""
        normalized_color = color.replace("_", "").lower()  # 小文字化 & `_` 削除

        if normalized_color not in self.NORMALIZED_COLORS:
            raise ValueError(f"Invalid color: {color}")

        actual_color = self.NORMALIZED_COLORS[normalized_color]  # 実際の色名を取得
        redVal, greenVal, blueVal = self.COLORS[actual_color]

        # 0-255 の値を PWM の 16bit (0-65535) に変換
        self.redLED.duty_u16(int(65535 / 255 * redVal))
        self.greenLED.duty_u16(int(65535 / 255 * greenVal))
        self.blueLED.duty_u16(int(65535 / 255 * blueVal))

    def off(self):
        """LED を消灯"""
        self.set_color("off")


# 使用例（スクリプトが直接実行された場合のみ動作）
if __name__ == "__main__":
    import utime

    led = RGBLED(15, 14, 13)  # GPIO 13, 14, 15xe に接続

    try:
        test_colors = [
            "RED", "Green", "blue", "Cyan", "Magenta",
            "YELLOW", "Orange", "PURPLE", "PiNk", "Lime",
            "BROWN", "Gray", "Light_Gray", "darkgray", "white",
            "Off"
        ]
        
        for color in test_colors:
            print(f"Setting color: {color}")
            led.set_color(color)
            utime.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        led.off()
