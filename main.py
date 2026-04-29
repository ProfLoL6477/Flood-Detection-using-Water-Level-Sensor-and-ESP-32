import network
import machine
import time
from BlynkLib import Blynk
import umail

ssid = 'Room-301'
password = 'etrx@301'
auth_token = 'TmqimPmM9HE1UnnGtbkH-X7R2yGjdiOV'

sender_email = 'iiot36855@gmail.com'
sender_name = 'ESP32'

sender_app_password = 'tdnrkofarjfvvurg'
recipient_email = 'warad.teni22@spit.ac.in'

email_subject = 'Flood Alert: Water Level Exceeded Threshold'

water_level_pin = machine.ADC(machine.Pin(34))
water_level_pin.atten(machine.ADC.ATTN_11DB)

blynk = Blynk(auth_token)

THRESHOLD = 2000

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not station.isconnected():
    time.sleep(1)

print("Wi-Fi Connected!")
print(station.ifconfig())

# Calibration function
def calibrate_sensor(raw_value):
    max_raw = 4095
    calibrated_max = 3000
    calibrated_value = min(int((raw_value / max_raw) * calibrated_max), calibrated_max)
    return calibrated_value

# Smoothed water level reading
def read_smoothed_water_level(samples=5, delay=10):
    total = 0
    for _ in range(samples):
        total += water_level_pin.read()
        time.sleep_ms(delay)
    return total // samples

# Email sending function
def send_email(water_level_value):
    try:
        print("Connecting to SMTP server...")
        smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
        print("Connected successfully. Logging in...")
        smtp.login(sender_email, sender_app_password)
        print("Logged in successfully. Preparing email...")
        smtp.to(recipient_email)
        smtp.write("From: {} <{}>\n".format(sender_name, sender_email))
        smtp.write("Subject: {}\n".format(email_subject))
        smtp.write("Flood Alert!\nWater Level is too high: {}\nPlease take necessary action.\n".format(water_level_value))
        print("Sending email...")
        smtp.send()
        smtp.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main water level monitoring function
def send_water_level():
    raw_value = read_smoothed_water_level()
    calibrated_value = calibrate_sensor(raw_value)
    print(f"Water Level Value: {calibrated_value}")
    
    # Send calibrated data to Blynk (Virtual Pin V4)
    blynk.virtual_write(4, calibrated_value)
    
    if calibrated_value > THRESHOLD:
        print("Flood detected! Sending email alert.")
        send_email(calibrated_value)

# Main loop
try:
    while True:
        blynk.run()
        send_water_level()
        time.sleep(5)
except Exception as e:
    print(f"Program Error: {e}")
finally:
    print("Program stopped.")
