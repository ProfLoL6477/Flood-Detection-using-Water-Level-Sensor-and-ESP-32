import network
import esp
import time
esp.osdebug(None)
ssid = '404_Not_Found'
password = '403_Forbidden'
# Connect to Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while not station.isconnected():
time.sleep(1)
print('Connection successful')
print(station.ifconfig())
