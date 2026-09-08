/* ============================================================
   GreenGrid AI — Hardware Test 06: FastAPI HTTP POST Ingestion Test
   File: iot/tests/06_test_api.ino
   ============================================================ */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
const char* API_URL       = "http://192.168.1.100:8000/api/iot/energy"; // Use laptop IPv4
const char* DEVICE_ID     = "ESP32-001";

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- GreenGrid AI: Test 06 - FastAPI Ingestion ---");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n[OK] Wi-Fi Connected!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    StaticJsonDocument<256> doc;
    doc["device_id"]       = DEVICE_ID;
    doc["timestamp"]       = "2026-08-24T12:00:00Z";
    doc["temperature"]     = 32.4;
    doc["humidity"]        = 65.0;
    doc["light_intensity"] = 750.0;
    doc["voltage"]         = 12.1;
    doc["current"]         = 1.8;
    doc["power"]           = 21.78;

    String jsonPayload;
    serializeJson(doc, jsonPayload);

    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");

    Serial.print("[POST] Transmitting payload to ");
    Serial.println(API_URL);

    int httpCode = http.POST(jsonPayload);
    if (httpCode > 0) {
      String response = http.getString();
      Serial.printf("[HTTP] Code: %d | Response: %s\n", httpCode, response.c_str());
    } else {
      Serial.printf("[HTTP] Error: %s\n", http.errorToString(httpCode).c_str());
    }
    http.end();
  }
  delay(10000);
}
