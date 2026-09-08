"""
GreenGrid AI — Python ESP32 IoT Simulator
File: iot/simulator/esp32_simulator.py

Generates realistic sensor data packets conforming strictly to API_CONTRACT.md and DATA_DICTIONARY.md
and posts them to the FastAPI backend endpoint POST /api/iot/energy.
Useful for testing the end-to-end data pipeline without physical hardware.
"""

import time
import math
import random
import requests
from datetime import datetime, timezone

API_BASE_URL = "http://127.0.0.1:8000"
ENDPOINT = f"{API_BASE_URL}/api/iot/energy"
DEVICE_ID = "ESP32-001"

print("=" * 70)
print("GreenGrid AI -- Python ESP32 Telemetry Hardware Simulator")
print(f"Target Endpoint: {ENDPOINT}")
print(f"Device ID      : {DEVICE_ID}")
print("=" * 70)

step = 0
try:
    while True:
        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        
        # Simulate realistic day-night cycles and environmental fluctuations
        sine_wave = math.sin(step * 0.1)
        temp = round(30.0 + (sine_wave * 4.0) + random.uniform(-0.5, 0.5), 1)
        hum = round(60.0 - (sine_wave * 8.0) + random.uniform(-1.0, 1.0), 1)
        light = round(max(0.0, 750.0 + (sine_wave * 250.0) + random.uniform(-20, 20)), 1)
        volt = round(12.0 + random.uniform(-0.2, 0.3), 1)
        curr = round(max(0.0, 1.5 + (sine_wave * 0.5) + random.uniform(-0.1, 0.1)), 2)
        power = round(volt * curr, 2)

        payload = {
            "device_id": DEVICE_ID,
            "timestamp": now_iso,
            "temperature": temp,
            "humidity": hum,
            "light_intensity": light,
            "voltage": volt,
            "current": curr,
            "power": power
        }

        print(f"\n[SIM] Sending Telemetry Packet (Step #{step+1})...")
        print(f"      Temp: {temp}°C | Hum: {hum}% | Light: {light} | V: {volt}V | I: {curr}A | P: {power}W")

        try:
            res = requests.post(ENDPOINT, json=payload, timeout=5)
            if res.status_code in [200, 201]:
                print(f"[OK] Response ({res.status_code}): {res.json()}")
            else:
                print(f"[FAIL] HTTP {res.status_code}: {res.text}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Could not connect to FastAPI server at {ENDPOINT}: {e}")

        step += 1
        time.sleep(5) # Send telemetry every 5 seconds

except KeyboardInterrupt:
    print("\n[STOP] Simulator terminated by user.")
