import time
import machine
from machine import Pin
import dht
import network
import ujson
from umqtt.simple import MQTTClient
import BlynkLib
import BlynkTimer


# MQTT Server Parameters
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER    = "broker.mqttdashboard.com"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "wokwi-weather"

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
  print(".", end="")
  time.sleep(0.1)
print(" Connected!")

print("Connecting to MQTT server... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.connect()

print("Connected!")

# Thay thế bằng chân nơi chân dữ liệu DHT22 được kết nối với ESP32
DHT22_PIN = 15

# Khởi tạo cảm biến DHT22
sensor = dht.DHT22(Pin(DHT22_PIN))

ledGreen = Pin(26, Pin.OUT)
ledRed = Pin(27, Pin.OUT)

switch_pin = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

# Kết nối động cơ servo vào chân GPIO 12
servo_pin = machine.Pin(4)

# Tạo đối tượng PWM để điều khiển động cơ servo
servo_pwm = machine.PWM(servo_pin, freq=50)

# Hàm để xoay động cơ servo đến góc cụ thể
def set_servo_angle(angle):
    duty = (angle / 180.0) * 102 + 26
    servo_pwm.duty(int(duty))

# Xác định chân LED RGB
rgbLedRed = Pin(32, Pin.OUT)
rgbLedGreen = Pin(33, Pin.OUT)
rgbLedBlue = Pin(25, Pin.OUT)

time.sleep(1)

# Gắn token của Blynk để kết nối
BLYNK_AUTH_TOKEN = "EtYdkLhAaHAdHYlY6n9p82ILMvQI5Uxn"
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

V_TEMP = 1
V_SWITCHLED = 2
V_LedWarning = 3
V_Humidity = 4

switch_state = 1  

rgbLedRed.on()
rgbLedGreen.off()
rgbLedBlue.off()

@blynk.on("V0")
def v0_read_handler(value):
    global switch_state
    if int(value[0]) == 0:
        # RGB màu đỏ
        rgbLedRed.off()
        rgbLedGreen.on()
        rgbLedBlue.off()
        switch_state = 0
    else:
        # RGB màu xanh lá
        rgbLedRed.on()
        rgbLedGreen.off()
        rgbLedBlue.off()
        switch_state = 1

while True:
    try:
        # Connect Blynk
        blynk.run()
        # Đọc giá trị trạng thái của slideSwitch
        # switch_state = switch_pin.value()
        print("Switch is: {}".format("OFF" if switch_state else "ON"))
        
        blynk.virtual_write(V_SWITCHLED, switch_state)

        # Đọc dữ liệu nhiệt độ và độ ẩm từ cảm biến
        sensor.measure()

        # Lấy giá trị nhiệt độ và độ ẩm
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Đưa giá trị nhiệt và độ ẩm đọc được lên Blynk
        blynk.virtual_write(V_TEMP, temperature)
        blynk.virtual_write(V_Humidity, humidity)

        # In giá trị nhiệt độ và độ ẩm
        print("Temperature: {}C".format(temperature))
        print("Humidity: {}%".format(humidity))
        print()  

        # Đợi một lúc trước khi đọc lần tiếp theo
        time.sleep(1)

        # Điều kiền về nhiệt độ để hiện trên led và bật động cơ servo
        if temperature > 30:
            ledGreen.off()
            ledRed.on()
            time.sleep(2)
            ledRed.off()
            set_servo_angle(0)
            
        elif temperature <= 30:
            ledRed.off()
            ledGreen.on()
            set_servo_angle(90)

        # Kiểm tra xem người dùng có cho phép hệ thống hoạt động không
        if switch_state == 1: 
            set_servo_angle(90)


    except Exception as e:
        # Nếu xảy ra lỗi khi đọc dữ liệu cảm biến, hãy in thông báo lỗi
        print("Error reading sensor data: {}".format(e))
        time.sleep(5)