import time
import machine
from machine import Pin, PWM, I2C
import dht
import network
import BlynkLib
import BlynkTimer
import ssd1306

# Định nghĩa các chân kết nối
DHT22_PIN = 15
LED_GREEN_PIN = 26
LED_RED_PIN = 27
SWITCH_PIN = 12
SERVO_PIN = 4
RGB_LED_RED_PIN = 32
RGB_LED_GREEN_PIN = 33
RGB_LED_BLUE_PIN = 25

# Định nghĩa các chân ảo Blynk
V_SYSTEM = 0
V_LED_FIRE = 1
V_FIRE_SUPPRESSTION = 2
V_TEMP = 3

oled_width = 128
oled_height = 64

# Cài đặt thông tin kết nối WiFi
WIFI_SSID = 'Wokwi-GUEST'
WIFI_PASSWORD = ''

# Cài đặt thông tin Blynk
BLYNK_TEMPLATE_ID = "TMPL69x6MPBw7"
BLYNK_TEMPLATE_NAME = "Quickstart Template"
BLYNK_AUTH_TOKEN = "ESxHtNueyvy26Uv_n4pHIfayZDRZK_pI"

# Kết nối WiFi
def connect_wifi(ssid, password):
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")

# Hàm để xoay động cơ servo đến góc cụ thể
def set_servo_angle(angle):
    duty = (angle / 180.0) * 102 + 26
    servo_pwm.duty(int(duty))

# Hàm hiển thị loading trên OLED
def show_loading():
    oled.fill(0)  
    oled.text("Loading...", 10, 10)
    oled.text("Please do not", 10, 30)
    oled.text("disconnect !", 10, 40)
    oled.show()  

# Hàm hiển thị chế độ hệ thống đã sẵn sàng
def system_ready():

    oled.fill(0)  
    oled.text("Please do not", 10, 10)
    oled.text("interact with", 10, 20)
    oled.text("the system at", 10, 30)
    oled.text("this time !", 10, 40)
    oled.show()

    time.sleep(2)
    oled.fill(0)  
    oled.text("This is a fire", 10, 10)
    oled.text("warning system,", 10, 20)
    oled.show()

    time.sleep(1)
    oled.fill(0)  
    oled.text("when the", 10, 10)
    oled.text("temperature is", 10, 20)
    oled.text("higher than", 10, 30)
    oled.text("50 degrees", 10, 40)
    oled.show()

    time.sleep(1)
    oled.fill(0)  
    oled.text("Blynk can be", 10, 10)
    oled.text("used to monitor", 10, 20)
    oled.text("and control the", 10, 30)
    oled.text("system", 10, 40)
    oled.show()

    time.sleep(1)
    oled.fill(0)  
    oled.text("In particular,", 10, 10)
    oled.text("RGB LEDs can", 10, 20)
    oled.text("only be controlled", 10, 30)
    oled.text("via Blynk", 10, 40)
    oled.show()
    
    time.sleep(1)
    oled.fill(0)  
    oled.text("System Ready !", 10, 10) 
    oled.show()


# Khởi tạo i2c
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

# Khởi tạo OLED
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Khởi tạo cảm biến DHT22
sensor = dht.DHT22(Pin(DHT22_PIN))

# Khởi tạo các chân LED và công tắc
ledGreen = Pin(LED_GREEN_PIN, Pin.OUT)
ledRed = Pin(LED_RED_PIN, Pin.OUT)
switch_pin = Pin(SWITCH_PIN, Pin.IN, Pin.PULL_UP)

# Khởi tạo chân điều khiển động cơ servo
servo_pwm = PWM(Pin(SERVO_PIN), freq=50)

# Khởi tạo chân LED RGB
rgbLedRed = Pin(RGB_LED_RED_PIN, Pin.OUT)
rgbLedGreen = Pin(RGB_LED_GREEN_PIN, Pin.OUT)
rgbLedBlue = Pin(RGB_LED_BLUE_PIN, Pin.OUT)

# Hiển thị chế độ loading khi hệ thống đang tải dữ liệu
show_loading()

# Thiết lập màu ban đầu cho LED RGB
rgbLedRed.off()
rgbLedGreen.off()
rgbLedBlue.off()

# Hàm kết nối WiFi
connect_wifi(WIFI_SSID, WIFI_PASSWORD)

# Hàm kết nối Blyk
blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

# Xử lý sự kiện Blynk
@blynk.on("V4")
def v4_read_handler(value):
    try:
        color_code = int(value[0])

        if color_code == 1:
            # Đổi màu LED RGB sang đỏ
            rgbLedRed.on()
            rgbLedGreen.off()
            rgbLedBlue.off()
            oled.fill(0)
            oled.text("LED RED ON", 10, 10)
            oled.show()
            time.sleep(2)
        elif color_code == 2:
            # Đổi màu LED RGB sang xanh lá
            rgbLedRed.off()
            rgbLedGreen.on()
            rgbLedBlue.off()
            oled.fill(0)
            oled.text("LED GREEN ON", 10, 10)
            oled.show()
            time.sleep(2)
        elif color_code == 3:
            # Đổi màu LED RGB sang xanh dương
            rgbLedRed.off()
            rgbLedGreen.off()
            rgbLedBlue.on()
            oled.fill(0)
            oled.text("LED BLUE ON", 10, 10)
            oled.show()
            time.sleep(2)
        else:
            # Tắt tất cả các màu
            rgbLedRed.off()
            rgbLedGreen.off()
            rgbLedBlue.off()
            oled.fill(0)
            oled.text("LED OFF", 10, 10)
            oled.show()
            time.sleep(2)

    except Exception as e:
        print("Error handling V4 value:", e)

# Hiển thị chế độ đã sẵn sàng kết nối
system_ready()

while True:
    try:

        # Kết nối Blynk
        blynk.run()

        # Đọc giá trị trạng thái của slideSwitch
        switch_state = switch_pin.value()

        # Đọc và gửi trạng thái công tắc lên Blynk
        print("Switch is: {}".format("OFF" if switch_state else "ON"))
        if switch_state == 0:
            blynk.virtual_write(V_SYSTEM, 1)
        else:
            blynk.virtual_write(V_SYSTEM, 0)

        # Đọc dữ liệu nhiệt độ và độ ẩm từ cảm biến DHT22
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()

        # Gửi dữ liệu nhiệt độ và độ ẩm lên Blynk
        blynk.virtual_write(V_TEMP, temperature)

        # In ra giá trị nhiệt độ và độ ẩm
        print("Temperature: {}C".format(temperature))
        print("Humidity: {}%".format(humidity))
        print()

        # Điều khiển LED và động cơ servo dựa vào nhiệt độ
        if temperature > 50:
            ledGreen.off()
            ledRed.on()
            time.sleep(2)
            ledRed.off()
            blynk.virtual_write(V_LED_FIRE, 1)
            oled.fill(0)
            oled.text("Fire Alert !", 10, 10)
            oled.text("Please activate", 10, 30)
            oled.text("the physical", 10, 40)
            oled.text("switch !", 10, 50)
            oled.show()
            if switch_state == 0:
                set_servo_angle(0)
                blynk.virtual_write(V_FIRE_SUPPRESSTION, "Active")
                oled.fill(0)
                oled.text("Fire Fighting !", 10, 10)
                oled.show()
        else:
            ledRed.off()
            ledGreen.on()
            set_servo_angle(90)
            blynk.virtual_write(V_LED_FIRE, 0)
            blynk.virtual_write(V_FIRE_SUPPRESSTION, "None")
            oled.fill(0)
            oled.text("Status: Stable", 10, 10)
            oled.text("Temp: {}C".format(temperature), 10, 30)
            oled.text("Humi: {}%".format(humidity), 10, 50)
            oled.show()

        # Đợi một khoảng thời gian trước khi đọc dữ liệu tiếp theo
        time.sleep(1)

    except Exception as e:
        # Nếu xảy ra lỗi khi đọc dữ liệu cảm biến, hãy in thông báo lỗi
        print("Error reading sensor data: {}".format(e))
        time.sleep(5)
