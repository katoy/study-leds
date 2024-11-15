from flask import Flask, render_template, request
from gpiozero import LED, CPUTemperature

# Flask アプリケーションの初期化
app = Flask(__name__)

# GPIOピンの設定
led = LED(17)  # GPIO 17 に接続されたLEDを制御
cpu = CPUTemperature()  # CPU 温度を取得するためのオブジェクト

@app.route("/")
def index():
    """LED 制御用のホームページを表示"""
    # 現在のLEDの状態を取得
    led_state = "ON" if led.is_lit else "OFF"
    # CPU温度を取得
    cpu_temp = round(cpu.temperature, 2)  # 温度を小数点第 2 位で丸める
    return render_template("index.html", led_state=led_state, cpu_temp=cpu_temp)

@app.route("/led", methods=["POST"])
def led_control():
    """LED のオン/オフを制御"""
    action = request.form.get("action")
    if action == "on":
        led.on()
    elif action == "off":
        led.off()
    
    # 現在の LED 状態と CPU 温度を取得してページを再描画
    led_state = "ON" if led.is_lit else "OFF"
    cpu_temp = round(cpu.temperature, 2)
    return render_template("index.html", led_state=led_state, cpu_temp=cpu_temp)

if __name__ == "__main__":
    try:
        # Flask アプリケーションを起動
        app.run(host="0.0.0.0", port=5000, debug=True)
    except KeyboardInterrupt:
        print("サーバーを終了します。")

