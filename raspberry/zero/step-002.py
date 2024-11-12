from gpiozero import PWMLED
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

# pigpioを利用するためのファクトリを設定
factory = PiGPIOFactory()

# GPIO 17 ピンを制御する PWM LED オブジェクトを作成
led = PWMLED(17, pin_factory=factory)

try:
    while True:
        # LEDを徐々に明るく
        sleep(0.5)
        for brightness in range(0, 101):  # 0% から 100% まで
            led.value = brightness / 100  # 0 から 1 の範囲に変換
            sleep(0.01)                   # 少し待機

        # LEDを徐々に暗く
        for brightness in range(100, -1, -1):  # 100% から 0% まで
            led.value = brightness / 100       # 0 から 1 の範囲に変換
            sleep(0.01)                        # 少し待機

except KeyboardInterrupt:
    # Ctrl + C が押された時に実行
    print("終了します")
    led.off()           # LED を OFF にして終了

