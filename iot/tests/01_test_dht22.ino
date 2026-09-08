/* ============================================================
   GreenGrid AI — Hardware Test 01: DHT22 Sensor Module (3-Pin)
   File: iot/tests/01_test_dht22.ino
   
   Hardware Connections:
   - DHT22 '+' (VCC)  -> ESP32 3.3V (or 5V)
   - DHT22 '-' (GND)  -> ESP32 GND
   - DHT22 'out' (DATA) -> ESP32 GPIO 4
   ============================================================ */

#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- GreenGrid AI: Test 01 - DHT22 Sensor ---");
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("[ERROR] Failed to read from DHT22 sensor! Check wiring.");
  } else {
    Serial.print("Temperature: ");
    Serial.print(temp, 1);
    Serial.print(" °C  |  Humidity: ");
    Serial.print(hum, 1);
    Serial.println(" %");
  }

  delay(2000);
}
