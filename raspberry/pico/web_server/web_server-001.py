import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

def load_config():
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

def connect(max_retries=10):
    ssid, password = load_config()
    if not ssid or not password:
        print("SSIDまたはPASSWORDが無効です")
        machine.reset()
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(ssid, password)

    for retry in range(max_retries):
        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f"Connected on {ip}")
            return ip
        print(f"Waiting for connection... ({retry + 1}/{max_retries})")
        sleep(1)
    
    print("Failed to connect to Wi-Fi after multiple attempts.")
    raise RuntimeError("Wi-Fi connection failed")

def open_socket(ip):
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    print("Socket open and listening on port 80")
    return connection

def load_template():
    try:
        with open('template-001.html', 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading template-001.html: {e}")
        wlan = network.WLAN(network.STA_IF)
        wlan.active(False)
        machine.reset()

def load_favicon():
    try:
        with open('favicon.ico', 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Error loading favicon.ico: {e}")
        return None

def get_led_state():
    return "ON" if pico_led.value else "OFF"

def webpage(template, temperature, state):
    return template.replace("{temperature}", str(temperature)).replace("{state}", state)

def serve(connection, favicon):
    template = load_template()

    while True:
        client = None
        try:
            client, _ = connection.accept()
            request = client.recv(1024).decode()
            print(f"Received request: {request}")

            request_line = request.split("\r\n")[0]
            method, path, _ = request_line.split(" ")
            path = path.split('?')[0]

            if path == '/favicon.ico':
                if favicon:
                    client.send("HTTP/1.1 200 OK\r\nContent-Type: image/x-icon\r\n\r\n")
                    client.sendall(favicon)
                else:
                    client.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nFavicon not found")
            elif path == '/lighton':
                pico_led.on()
            elif path == '/lightoff':
                pico_led.off()

            state = get_led_state()
            temperature = pico_temp_sensor.temp

            if path in ['/lighton', '/lightoff', '/']:
                html = webpage(template, temperature, state)
                client.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
            else:
                client.send("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>")
        except Exception as e:
            print(f"Error: {e}")
            if client:
                client.send("HTTP/1.1 500 Internal Server Error\r\n\r\n<h1>500 Internal Server Error</h1>")
        finally:
            if client:
                client.close()

try:
    ip = connect(max_retries=10)
    favicon = load_favicon()
    connection = open_socket(ip)
    serve(connection, favicon)
except RuntimeError as e:
    print(e)
    print("Program exiting...")
finally:
    print("Cleaning up resources...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    machine.reset()
