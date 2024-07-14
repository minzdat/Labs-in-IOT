#include <Arduino.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <DHT.h> 

// WiFi Credentials
#define WIFI_SSID "Wokwi-GUEST"
#define WIFI_PASSWORD ""

// Firebase things
#define DATABASE_URL "https://lab-4-esp-firebase-default-rtdb.asia-southeast1.firebasedatabase.app/"
HTTPClient client;

// Pins definition
#define trigPin 25
#define echoPin 33
#define ledV 2
LiquidCrystal_I2C LCD = LiquidCrystal_I2C(0x27, 16, 2);

// DHT sensor setup
#define DHTPIN 13     
#define DHTTYPE DHT22 

DHT dht(DHTPIN, DHTTYPE);

// Variables
int prevDistance = 0;
int prevTemperature = 0;
int prevHumidity = 0;
String payload = "";
String ledVBool;

void setup()
{
  Serial.begin(115200);

  LCD.init();
  LCD.backlight();
  LCD.setCursor(0, 0);
  LCD.print("Connecting to ");
  LCD.setCursor(0, 1);
  LCD.print("WiFi ");

  // WIFI
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected: ");
  Serial.println(WiFi.localIP());

  LCD.clear();
  LCD.setCursor(0, 0);
  LCD.println("Online");
  delay(500);
  LCD.clear();
  LCD.setCursor(0, 0);
  LCD.println("Connecting to");
  LCD.setCursor(0, 1);
  LCD.println("Firebase...");
  Serial.println("Connecting...");

  // Firebase
  client.begin(DATABASE_URL);
  int httpResponseCode = client.GET();

  if (httpResponseCode > 0)
  {
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.println("Connected");
    Serial.println("Connected, Firebase payload:");
    payload = client.getString();
    Serial.println(payload);
    Serial.println();
  }

  // Components
  pinMode(trigPin, OUTPUT); // Set as output
  pinMode(echoPin, INPUT);  // Set as input
  pinMode(ledV, OUTPUT);

  for (int i = 0; i < 5; i++)
  {
    digitalWrite(ledV, HIGH);
    delay(200);
    digitalWrite(ledV, LOW);
    delay(200);
  }

  // DHT sensor start
  dht.begin();
}

void loop()
{
  // Distance measurement with HCSR04
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(2);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1;

  // DHT temperature and humidity readings
  int temperature = dht.readTemperature(); 
  int humidity = dht.readHumidity();     

  // Update Firebase with DataSensor data
  String pathDataSensor = String(DATABASE_URL) + "/DataSensor.json";
  client.begin(pathDataSensor);
  DynamicJsonDocument doc(200);
  doc["Temperature"] = temperature;
  doc["Humidity"] = humidity;
	doc["Distance"] = distance;
  
  String json;
  serializeJson(doc, json);
  int httpCodeDataSensor = client.PUT(json);

  if (httpCodeDataSensor > 0)
  {
    if (httpCodeDataSensor == HTTP_CODE_OK)
    {
      Serial.println("DataSensor PUT request successful");
			LCD.clear();
			LCD.setCursor(0, 0);
			LCD.print("PUT successful");
      delay(1000);
    }
    else
    {
      Serial.println("DataSensor PUT request failed with error: " + String(httpCodeDataSensor));
    	LCD.clear();
			LCD.setCursor(0, 0);
			LCD.print("PUT failed");
      delay(1000);
    }
  }
  else
  {
    Serial.println("DataSensor PUT request failed with error: " + String(client.errorToString(httpCodeDataSensor).c_str()));
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.print("PUT failed");
    delay(1000);
  }

  // Firebase GET request to update LCD
  String pathGet = String(DATABASE_URL) + ".json";
  client.begin(pathGet);
  int httpCodeGet = client.GET();

  if (httpCodeGet > 0)
  {
    if (httpCodeGet == HTTP_CODE_OK)
    {
      String payload = client.getString();
      Serial.println("GET request successful: " + payload);

      // Parse JSON
      DynamicJsonDocument doc(1024);  // Adjust the size as necessary
      DeserializationError error = deserializeJson(doc, payload);

      // Access Temperature, Humidity, and Distance
      int temperatureGetData = doc["DataSensor"]["Temperature"];
      int humidityGetData = doc["DataSensor"]["Humidity"];
      int distanceGetData = doc["DataSensor"]["Distance"];

      LCD.clear();
			LCD.setCursor(0, 0);
			LCD.print("GET successful");
      delay(1000);

      // Update LCD with received data
			LCD.clear();
			LCD.setCursor(0, 0);
			LCD.print("Temp:");
			LCD.print(temperatureGetData); 
			LCD.print("C");
			LCD.setCursor(8, 0);
			LCD.print("Humi:");
			LCD.print(humidityGetData);
			LCD.print("%");

			LCD.setCursor(0, 1);
			LCD.print("Dist: ");
			LCD.print(distanceGetData);
			LCD.print(" cm");

      if (temperatureGetData >= 30 || humidityGetData <= 20 || distanceGetData <= 30)
      {
        digitalWrite(ledV, HIGH);
      }
      else
      {
        digitalWrite(ledV, LOW);
      }
    }
    else
    {
      Serial.println("GET request failed with error: " + String(httpCodeGet));
      LCD.clear();
			LCD.setCursor(0, 0);
			LCD.print("GET failed");
      delay(1000);
    }
  }
  else
  {
    Serial.println("GET request failed with error: " + String(client.errorToString(httpCodeGet).c_str()));
    LCD.clear();
    LCD.setCursor(0, 0);
    LCD.print("GET failed");
    delay(1000);
  }

  delay(500);
}
