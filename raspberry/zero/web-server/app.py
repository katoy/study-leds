# 配線
# GPIO 17 --- [アノード (+)]LED[カソード (-)] --- [抵抗] --- GND
#
# 抵抗（330Ω ～ 1kΩ)
#

from flask import Flask, request, jsonify, render_template
from gpiozero import LED, CPUTemperature

# Flask アプリケーションの初期化
app = Flask(__name__)

# GPIO ピンの設定
led = LED(17)  # GPIO 17 に接続された LED を制御
cpu = CPUTemperature()  # CPU 温度を取得するためのオブジェクト

@app.route("/")
def index():
    """
    LED 制御用のホームページを表示
    """
    # 現在の LED 状態と CPU 温度を取得
    led_state = "ON" if led.is_lit else "OFF"
    cpu_temp = round(cpu.temperature, 2)  # 温度を小数点第 2 位で丸める
    return render_template("index.html", led_state=led_state, cpu_temp=cpu_temp)

@app.route("/led", methods=["POST"])
def led_control():
    """
    JSON データを受け取り LED のオン/オフを制御
    """
    if request.content_type != "application/json":
        return jsonify({"error": "Unsupported Media Type"}), 415

    try:
        data = request.get_json()  # JSON データを取得
        print("Received JSON:", data)  # デバッグ用
        action = data.get("action")  # "action" キーを取得

        if action == "on":
            led.on()
            print("LED is turned ON")
        elif action == "off":
            led.off()
            print("LED is turned OFF")
        else:
            return jsonify({"error": "Invalid action"}), 400

        # 現在の LED 状態を返す
        led_state = "ON" if led.is_lit else "OFF"
        return jsonify({"led_state": led_state}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Invalid request"}), 400

if __name__ == "__main__":
    try:
        # Flask アプリケーションを起動
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        pass


