import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

def load_config():
    """テキストファイルからSSIDとパスワードを読み込む"""
    config = {}
    try:
        with open('config.txt', 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
        return config.get('SSID'), config.get('PASSWORD')
    except Exception as e:
        print(f"Error loading config.txt: {e}")
        machine.reset()

def connect():
    """WLANに接続"""
    ssid, password = load_config()
    if not ssid or not password:
        print("SSIDまたはPASSWORDが無効です")
        machine.reset()
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)
    
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def open_socket(ip):
    """ソケットを開く"""
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def load_template():
    """HTMLテンプレートをファイルから読み込む"""
    try:
        with open('template.html', 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading template.html: {e}")
        machine.reset()

def webpage(template, temperature, state):
    """HTMLを生成"""
    return template.replace("{temperature}", str(temperature)).replace("{state}", state)

def serve(connection):
    """Webサーバーを開始"""
    state = 'OFF'
    pico_led.off()
    temperature = 0
    template = load_template()

    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)

        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request == '/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp

        html = webpage(template, temperature, state)
        client.send(html)

        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
