import machine
import utime
import ssd1306
import time
 
sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0,sda=sda, scl=scl, freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
 
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

# JST (UTC+9) のタイムゾーンオフセット（秒単位）
JST_OFFSET = 9 * 60 * 60  # 9時間 * 60分 * 60秒

while True:
    oled.fill(0)
    reading = sensor_temp.read_u16() * conversion_factor
    # The temperature sensor measures the Vbe voltage of a biased bipolar diode, connected to the fifth ADC channel
    # Typically, Vbe = 0.706V at 27 degrees C, with a slope of -1.721mV (0.001721) per degree. 
    temperature = 27 - (reading - 0.706)/0.001721
    
    # 現在のUTC時刻を取得
    utc_time = time.time()
    # JST に変換
    jst_time = time.localtime(utc_time + JST_OFFSET)
    formatted_day = "{:04}-{:02}-{:02}".format(jst_time[0],jst_time[1], jst_time[2])
    formatted_time = "  {:02}:{:02}:{:02}".format(jst_time[3], jst_time[4], jst_time[5])
    
    oled.text("Temp:" + str(temperature), 0, 5)
    oled.text(formatted_day, 0, 20)
    oled.text(formatted_time, 0, 35)
    oled.show()
    
    utime.sleep(3)