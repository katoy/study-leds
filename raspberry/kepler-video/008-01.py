from picozero import LED, Pot
import utime

led_0 = LED(12)
led_1 = LED(13)
led_2 = LED(14)
potentiometer = Pot(28)

while True:
    # 電圧を取得 (picozeroのPotクラスは0〜1の値を返す)
    voltage = potentiometer.value * 3.3  # 3.3Vスケールに変換
    print(voltage)

    led_0.value = 0
    led_1.value = 0
    led_2.value = 0    
    if voltage < 80:
        led_0.value = 1
    elif voltage < 90:
        led_1.value = 1
    else:
        led_2.value = 1

    utime.sleep(0.5)
