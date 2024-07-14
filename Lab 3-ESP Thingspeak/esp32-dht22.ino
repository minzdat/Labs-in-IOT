#include <Arduino.h>
#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include "DHTesp.h"
#include "ThingSpeak.h"
#include "RTClib.h"

// Định nghĩa các hằng số
const int DHT_PIN = 19;
const char* WIFI_NAME = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";
const int myChannelNumber = 2598463;
const char* myApiKey = "6TFBWU9VR6A1EAI6";
const char* server = "api.thingspeak.com";

// Khởi tạo đối tượng LCD
LiquidCrystal_I2C LCD(0x27, 16, 2);
DHTesp dhtSensor;
WiFiClient client;
RTC_DS1307 rtc;

char daysOfTheWeek[7][12] = {"Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"};

void setup() {
  Serial.begin(115200); // Khởi động serial với tốc độ 115200

  // Khởi động LCD
  LCD.init();
  LCD.backlight();
  LCD.setCursor(0, 0);
  LCD.println("Truong Minh Dat");
  LCD.setCursor(0, 1);
  LCD.print("Loading...");
  delay(1000);

  // Khởi động cảm biến DHT
  dhtSensor.setup(DHT_PIN, DHTesp::DHT22);

  // Kết nối WiFi
  WiFi.begin(WIFI_NAME, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Wifi not connected");
  }
  Serial.println("Wifi connected!");
  Serial.println("Local IP: " + String(WiFi.localIP()));
  WiFi.mode(WIFI_STA);

  // Khởi động ThingSpeak
  ThingSpeak.begin(client);

  // Khởi động RTC
  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    Serial.flush();
    abort();
  }

  if (!rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    // Nếu RTC không chạy, thiết lập thời gian mặc định (ví dụ: 1/1/2020 00:00:00)
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }
}

void loop() {
  // Lấy thời gian hiện tại từ RTC
  DateTime now = rtc.now();

  // Hiển thị thời gian hiện tại lên Serial Monitor
  Serial.print("Current time: ");
  Serial.print(now.year(), DEC);
  Serial.print('/');
  Serial.print(now.month(), DEC);
  Serial.print('/');
  Serial.print(now.day(), DEC);
  Serial.print(" (");
  Serial.print(daysOfTheWeek[now.dayOfTheWeek()]);
  Serial.print(") ");
  Serial.print(now.hour(), DEC);
  Serial.print(':');
  Serial.print(now.minute(), DEC);
  Serial.print(':');
  Serial.print(now.second(), DEC);
  Serial.println();

  // Đọc dữ liệu từ cảm biến DHT
  TempAndHumidity data = dhtSensor.getTempAndHumidity();

  // Gửi dữ liệu đến ThingSpeak
  ThingSpeak.setField(1, data.temperature);
  ThingSpeak.setField(2, data.humidity);

  // Xóa màn hình LCD trước khi hiển thị dữ liệu mới
  LCD.clear();

  // Hiển thị dữ liệu lên LCD
  LCD.setCursor(0, 0);
  LCD.print("Temp: " + String(data.temperature) + "C");
  LCD.setCursor(0, 1);
  LCD.print("Humi: " + String(data.humidity) + "%");

  delay(1000);

  // Gửi dữ liệu đến ThingSpeak
  int response = ThingSpeak.writeFields(myChannelNumber, myApiKey);

  // Hiển thị dữ liệu lên Serial Monitor
  Serial.println("Temp: " + String(data.temperature, 1) + "°C");
  Serial.println("Humidity: " + String(data.humidity, 2) + "%");

  // Kiểm tra phản hồi từ ThingSpeak
  if (response == 200) {
    Serial.println("Data pushed successfully");
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.print("Date: " + String(now.year()) + "/" + String(now.month()) + "/" + String(now.day()));
    LCD.setCursor(0, 1);
    LCD.print("Time: " + String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second()));
    delay(2000);
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.println("ThingSpeak OK !");
  } else {
    Serial.println("Push error: " + String(response));
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.print("Date: " + String(now.year()) + "/" + String(now.month()) + "/" + String(now.day()));
    LCD.setCursor(0, 1);
    LCD.print("Time: " + String(now.hour()) + ":" + String(now.minute()) + ":" + String(now.second()));
    delay(2000);
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.println("Push error");
  }
  Serial.println("---");

  delay(1000); // Chờ 1 giây trước khi lặp lại
}
