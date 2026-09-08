/* ============================================================
   GreenGrid AI — Hardware Test 04: SSD1306 0.96" I2C OLED Display
   File: iot/tests/04_test_oled.ino
   
   Hardware Connections:
   - OLED GND -> ESP32 GND
   - OLED VDD -> ESP32 3.3V (or 5V)
   - OLED SCK -> ESP32 GPIO 22 (I2C SCL)
   - OLED SDA -> ESP32 GPIO 21 (I2C SDA)
   ============================================================ */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(115200);
  Serial.println("\n--- GreenGrid AI: Test 04 - OLED Display ---");
  Wire.begin(21, 22);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("[ERROR] SSD1306 OLED not found at 0x3C! Check I2C wiring.");
  } else {
    Serial.println("[OK] SSD1306 OLED display initialized successfully!");
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("   GREEN GRID AI");
    display.println("--------------------");
    display.println("Temp   : 31.5 C");
    display.println("Humid  : 58.0 %");
    display.println("Light  : 745");
    display.println("Voltage: 12.1 V");
    display.println("Current: 1.80 A");
    display.println("Power  : 21.78 W");
    display.display();
  }
}

void loop() {
  // Static screen display test
  delay(5000);
}
