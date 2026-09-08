/* ============================================================
   GreenGrid AI — Hardware Test 02: LDR Sensor Module (4-Pin)
   File: iot/tests/02_test_ldr.ino
   
   Hardware Connections:
   - LDR VCC -> ESP32 3.3V
   - LDR GND -> ESP32 GND
   - LDR AO  -> ESP32 GPIO 34 (Analog ADC1_CH6)
   - LDR DO  -> Unconnected (or GPIO 33 optional)
   ============================================================ */

#define LDR_AO_PIN 34

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- GreenGrid AI: Test 02 - LDR Sensor Module ---");
  analogSetAttenuation(ADC_11db); // Full 0-3.3V range
}

void loop() {
  int rawADC = analogRead(LDR_AO_PIN);
  float lightIntensity = (rawADC / 4095.0) * 1024.0; // Scaled to 0-1024 range

  Serial.print("Raw ADC (0-4095): ");
  Serial.print(rawADC);
  Serial.print("  |  Scaled Light Intensity (0-1024): ");
  Serial.println(lightIntensity, 1);

  delay(1000);
}
