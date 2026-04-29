import network
import esp
import time

esp.osdebug(None)

ssid = '404 Not Found'
password = '403'

# Connect to Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while not station.isconnected():
    time.sleep(1)

print('Connection successful')
print(station.ifconfig())
