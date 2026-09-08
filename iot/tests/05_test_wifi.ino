/* ============================================================
   GreenGrid AI — Hardware Test 05: ESP32 Wi-Fi Connectivity
   File: iot/tests/05_test_wifi.ino
   ============================================================ */

#include <WiFi.h>

const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- GreenGrid AI: Test 05 - Wi-Fi Connectivity ---");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi SSID: ");
  Serial.println(WIFI_SSID);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\n[OK] Wi-Fi Connected!");
  Serial.print("ESP32 Local IPv4 Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  delay(5000);
}
