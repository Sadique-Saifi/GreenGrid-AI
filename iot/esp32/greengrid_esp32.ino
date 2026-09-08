/* ============================================================
   GreenGrid AI — Dual Mode ESP32 Firmware (AP Hotspot + STA Station)
   File: iot/esp32/greengrid_esp32.ino
   
   Broadcasting AP Hotspot Name: "GreenGrid-ESP32" (Password: "12345678")
   You can see "GreenGrid-ESP32" directly in your Laptop/Phone Wi-Fi list!
   ============================================================ */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "DHT.h"

// ============================================================
// CONFIGURATION (Your Wi-Fi & Laptop IP)
// ============================================================
const char* WIFI_SSID     = "SQUAD-WiFi";                        // Router / Hotspot SSID
const char* WIFI_PASSWORD = "21712203";                          // Router / Hotspot Password
const char* API_BASE_URL  = "http://10.242.163.74:8000/api/iot/energy"; // Laptop IPv4
const char* DEVICE_ID     = "ESP32-001";

// ESP32 Broadcast Hotspot (Visible in laptop/phone Wi-Fi list!)
const char* AP_SSID       = "GreenGrid-ESP32";
const char* AP_PASSWORD   = "12345678";

#define DHTPIN 4
#define DHTTYPE DHT22
#define LDR_AO_PIN 34
#define VOLT_PIN 35
#define CURR_PIN 32
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
unsigned long lastTransmitTime = 0;
unsigned long lastWiFiRetryTime = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n==================================================");
  Serial.println("  GREEN GRID AI -- DUAL AP+STA ESP32 FIRMWARE    ");
  Serial.println("==================================================");

  analogSetAttenuation(ADC_11db);
  Wire.begin(21, 22);
  dht.begin();

  if (display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 5);
    display.println("  GREEN GRID AI");
    display.println("--------------------");
    display.println("Starting Wi-Fi...");
    display.display();
  }

  // Set Dual Mode: Broadcast AP Hotspot AND connect to SQUAD-WiFi
  WiFi.mode(WIFI_AP_STA);

  // 1. Broadcast visible Wi-Fi Access Point "GreenGrid-ESP32"
  bool apSuccess = WiFi.softAP(AP_SSID, AP_PASSWORD);
  if (apSuccess) {
    Serial.print("[AP] Broadcasting Wi-Fi Hotspot: '");
    Serial.print(AP_SSID);
    Serial.println("' (Pass: 12345678)");
    Serial.print("[AP] ESP32 AP IP Address: ");
    Serial.println(WiFi.softAPIP());
  }

  // 2. Connect to your local network "SQUAD-WiFi"
  connectWiFi();
}

void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  if (millis() - lastWiFiRetryTime < 10000 && lastWiFiRetryTime != 0) return;
  lastWiFiRetryTime = millis();

  Serial.print("[NET] Connecting to Wi-Fi: '");
  Serial.print(WIFI_SSID);
  Serial.println("'...");

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 12) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[OK] Wi-Fi Connected to SQUAD-WiFi!");
    Serial.print("[NET] ESP32 Station IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WARN] SQUAD-WiFi connecting... Broadcast AP 'GreenGrid-ESP32' is ACTIVE.");
  }
}

void updateOLED(float temp, float hum, float light, float volt, float curr, float power) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  display.setCursor(0, 0);
  display.println("   GREEN GRID AI");
  display.println("--------------------");
  
  display.print("Temp : "); display.print(temp, 1); display.println(" C");
  display.print("Humid: "); display.print(hum, 1); display.println(" %");
  display.print("Light: "); display.println((int)light);
  display.print("V: "); display.print(volt, 1); display.print("V  I: "); display.print(curr, 2); display.println("A");
  display.print("Power: "); display.print(power, 2); display.println(" W");

  // Show Wi-Fi status on bottom right
  display.setCursor(85, 56);
  if (WiFi.status() == WL_CONNECTED) {
    display.print("NET:OK");
  } else {
    display.print("AP:ON");
  }

  display.display();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  unsigned long currentMillis = millis();
  if (currentMillis - lastTransmitTime >= 5000) {
    lastTransmitTime = currentMillis;

    // 1. Read Sensors
    float temp = dht.readTemperature(); if (isnan(temp)) temp = 30.5;
    float hum  = dht.readHumidity();    if (isnan(hum))  hum  = 80.0;
    float lightIntensity = (analogRead(LDR_AO_PIN) / 4095.0) * 1024.0;
    float busVoltage = ((analogRead(VOLT_PIN) / 4095.0) * 3.3) * 5.0;
    float current_A = abs((((analogRead(CURR_PIN) / 4095.0) * 3.3) - 1.65) / 0.185);
    if (current_A < 0.05) current_A = 0.0;
    float power_W = busVoltage * current_A;

    // 2. Print Live Metrics
    Serial.printf("[SENSOR] Temp: %.1fC | Hum: %.1f%% | Light: %.0f | V: %.1fV | I: %.2fA | P: %.2fW\n",
                  temp, hum, lightIntensity, busVoltage, current_A, power_W);

    // 3. Refresh OLED
    updateOLED(temp, hum, lightIntensity, busVoltage, current_A, power_W);

    // 4. Send HTTP POST payload when connected
    if (WiFi.status() == WL_CONNECTED) {
      StaticJsonDocument<256> doc;
      doc["device_id"]       = DEVICE_ID;
      doc["timestamp"]       = "2026-08-25T12:00:00Z";
      doc["temperature"]     = round(temp * 10.0) / 10.0;
      doc["humidity"]        = round(hum * 10.0) / 10.0;
      doc["light_intensity"] = round(lightIntensity * 10.0) / 10.0;
      doc["voltage"]         = round(busVoltage * 10.0) / 10.0;
      doc["current"]         = round(current_A * 100.0) / 100.0;
      doc["power"]           = round(power_W * 100.0) / 100.0;

      String jsonPayload;
      serializeJson(doc, jsonPayload);

      HTTPClient http;
      http.begin(API_BASE_URL);
      http.addHeader("Content-Type", "application/json");

      Serial.print("[POST] Transmitting payload to ");
      Serial.print(API_BASE_URL);
      Serial.println("...");

      int httpCode = http.POST(jsonPayload);
      if (httpCode > 0) {
        String response = http.getString();
        Serial.printf("[HTTP] Status: %d | Server Response: %s\n", httpCode, response.c_str());
      } else {
        Serial.printf("[HTTP] POST Failed. Error: %s\n", http.errorToString(httpCode).c_str());
      }
      http.end();
    }
  }
}
