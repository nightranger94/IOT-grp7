import network
import urequests
import machine
import time
import math


#READ FIRST
#READ FIRST
#READ FIRST
#READ FIRST


# Somelines of code are commented out for code testing
# If program is wanted run as wanted remove "#" from intended code lines
# Also put correct credentials for wifi id, wifi password and api key

#READ FIRST
#READ FIRST
#READ FIRST
#READ FIRST


# wifi + apikey
SSID = "wifi id"
PASSWORD = "pw"
THINGSPEAK_API_KEY = "api key"


ldr_pin = machine.ADC(28)
led_pin = machine.Pin(15, machine.Pin.OUT)  

# PWM values
led_pwm = machine.PWM(led_pin)
led_pwm.freq(1000)

# Threshold for light intensity
threshold = 20000

count = 0

# wifi connection function
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print("Connected to Wi-Fi:", wlan.ifconfig())

# encrypt the light value (cube and then square root)
def process_light_value(light_value):
    cubed_value = light_value ** 3
    sqrt_value = math.sqrt(cubed_value)
    return int(sqrt_value) 

# adjusting led brightness using pwm
def adjust_led_brightness(light_value):
    """Adjust the brightness of the LED based on the light value."""
    if light_value < 5000:
        led_pwm.duty_u16(65535)
        
    elif 3000 <= light_value < 6000:
        led_pwm.duty_u16(32768)
        
    elif light_value >= 6000:
        led_pwm.duty_u16(6553) 

# send encrypted light value to thingspeak database
def send_to_thingspeak(processed_value):
    url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={processed_value}"
    try:
        response = urequests.get(url)
        print("ThingSpeak Response:", response.text)
        response.close()
    except Exception as e:
        print("Failed to send data to ThingSpeak:", e)
        
        

# MAIN PROGRAM
try:
    # Connect to Wi-Fi
    # connect_wifi(SSID, PASSWORD)

    while True:
        light_value = ldr_pin.read_u16()
        print("Light Intensity:", light_value)
        processed_value = process_light_value(light_value)
        print("Processed Light Value:", processed_value)
        adjust_led_brightness(light_value)
        # send_to_thingspeak(processed_value)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("Program stopped.")