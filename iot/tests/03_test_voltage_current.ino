/* ============================================================
   GreenGrid AI — Hardware Test 03: DC Voltage (0-25V) & Current Sensors
   File: iot/tests/03_test_voltage_current.ino
   
   Hardware Connections:
   - Voltage Sensor VCC -> ESP32 3.3V (Module power reference)
   - Voltage Sensor GND -> ESP32 GND & Solar/Battery Ground
   - Voltage Sensor OUT -> ESP32 GPIO 35 (ADC1_CH7)
   - Voltage Sensor Screw Terminals (+ / -) -> Solar Panel / Battery (+) & (-)
   - Current Sensor VCC -> ESP32 5V (VIN)
   - Current Sensor GND -> ESP32 GND
   - Current Sensor OUT -> ESP32 GPIO 32 (ADC1_CH4)
   ============================================================ */

#define VOLT_PIN 35
#define CURR_PIN 32

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- GreenGrid AI: Test 03 - DC Voltage & Current Sensors ---");
  analogSetAttenuation(ADC_11db);
}

void loop() {
  // Read Voltage Sensor (0-25V module uses 5:1 resistor divider)
  int rawVolt = analogRead(VOLT_PIN);
  float pinVoltage = (rawVolt / 4095.0) * 3.3;
  float measuredVoltage = pinVoltage * 5.0; // 5:1 scale factor

  // Read Current Sensor (ACS712 / ACS217 5A Module)
  int rawCurr = analogRead(CURR_PIN);
  float currPinVoltage = (rawCurr / 4095.0) * 3.3;
  // Offset centered at VCC/2 (approx 1.65V to 2.5V depending on VCC)
  float measuredCurrent = abs((currPinVoltage - 1.65) / 0.185); // 185mV/A sensitivity for 5A module

  float calculatedPower = measuredVoltage * measuredCurrent;

  Serial.print("Voltage: ");
  Serial.print(measuredVoltage, 2);
  Serial.print(" V  |  Current: ");
  Serial.print(measuredCurrent, 2);
  Serial.print(" A  |  Power: ");
  Serial.print(calculatedPower, 2);
  Serial.println(" W");

  delay(1500);
}
