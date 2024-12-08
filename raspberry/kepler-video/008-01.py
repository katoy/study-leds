from picozero import LED, Pot
import utime

led_0 = LED(12)
led_1 = LED(13)
led_2 = LED(14)
potentiometer = Pot(28)

while True:
    # 電圧を取得 (picozeroのPotクラスは0〜1の値を返す)
    voltage = potentiometer.value * 3.3  # 3.3Vスケールに変換
    # print(voltage)

    led_0.off()
    led_1.off()
    led_2.off()   
    if voltage < 1.0:
        led_0.on()
    elif 1.0 <= voltage < 2.0:
        led_1.on()
    else:
        led_2.on()

    utime.sleep(0.5)
