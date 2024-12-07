from picozero import LED
import utime

# 外部 LED を使う場合の指定
led_0 = LED(12)
led_1 = LED(13)
led_2 = LED(14)
led_3 = LED(15)

count = 0

while count < 16:
    # count を2 進数と 10 進数で表示
    print(f"{count:04b} {count:2d}")
    # `count` の最下位ビットで LED の状態を制御
    led_0.value = 1 if (count & 1) else 0
    led_1.value = 1 if (count & 2) else 0
    led_2.value = 1 if (count & 4) else 0
    led_3.value = 1 if (count & 8) else 0
    utime.sleep(1)

    # カウントをインクリメント
    count += 1

# 最後にすべての LED を消灯
led_0.off()
led_1.off()
led_2.off()
led_3.off()
print("All LEDs are OFF")
