import network
import socket
import secrets

# 1. Подключение к Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.ssid, secrets.password)

print("Connecting to WiFi...", end="")
while not wlan.isconnected():
    print(".", end="")
    import time
    time.sleep(1)
print("\nConnected!")
print("IP Address:", wlan.ifconfig()[0])

# 2. Настройка HTTP сервера
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Server listening on port 80...")

    while True:
        try:
            client, addr = s.accept()
            print('Got connection from %s' % str(addr[0]))
            request = client.recv(1024)
            with open('index.html', 'rb') as f:
                client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    client.send(chunk)
            client.close()
        except Exception as e:
            print("Error:", e)

try:
    start_server()
except KeyboardInterrupt:
    print("Server stopped")
