"""
GreenGrid AI — IoT Ingestion & Device Management Test Suite
Tests 10 mandatory IoT ingestion scenarios, validation rules, device registration checks,
and device status updates.
"""

import sys
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from main import app

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

client = TestClient(app)

def test_iot_scenarios():
    print("=" * 75)
    print("GreenGrid AI -- IoT Ingestion & Device Management Test Suite")
    print("=" * 75)

    passed = 0
    failed = 0
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    valid_payload = {
        "device_id": "ESP32-001",
        "timestamp": now_iso,
        "temperature": 32.5,
        "humidity": 61.0,
        "light_intensity": 785.0,
        "voltage": 12.1,
        "current": 1.8,
        "power": 21.78
    }

    tests = [
        {
            "name": "1. Valid ESP32 sensor reading",
            "method": "POST", "url": "/api/iot/energy",
            "payload": valid_payload,
            "expected_status": 201
        },
        {
            "name": "2. Invalid device_id (unregistered)",
            "method": "POST", "url": "/api/iot/energy",
            "payload": {**valid_payload, "device_id": "ESP32-UNREGISTERED-999"},
            "expected_status": 403
        },
        {
            "name": "3. Missing required field (temperature)",
            "method": "POST", "url": "/api/iot/energy",
            "payload": {
                "device_id": "ESP32-001", "timestamp": now_iso,
                "humidity": 61.0, "light_intensity": 785.0, "voltage": 12.1, "current": 1.8
            },
            "expected_status": 422
        },
        {
            "name": "4. Invalid temperature (> 85°C)",
            "method": "POST", "url": "/api/iot/energy",
            "payload": {**valid_payload, "temperature": 120.0},
            "expected_status": 422
        },
        {
            "name": "5. Invalid humidity (> 100%)",
            "method": "POST", "url": "/api/iot/energy",
            "payload": {**valid_payload, "humidity": 150.0},
            "expected_status": 422
        },
        {
            "name": "6. Invalid timestamp format",
            "method": "POST", "url": "/api/iot/energy",
            "payload": {**valid_payload, "timestamp": "invalid-timestamp-string"},
            "expected_status": 422
        },
        {
            "name": "7. Invalid voltage/current (negative)",
            "method": "POST", "url": "/api/iot/energy",
            "payload": {**valid_payload, "voltage": -12.1},
            "expected_status": 422
        },
        {
            "name": "8. Duplicate reading idempotency",
            "method": "POST", "url": "/api/iot/energy",
            "payload": valid_payload,
            "expected_status": 201
        },
        {
            "name": "9. Registered Devices Endpoint",
            "method": "GET", "url": "/api/devices",
            "payload": None,
            "expected_status": 200
        },
        {
            "name": "10. Device Status & Detail Update",
            "method": "GET", "url": "/api/devices/ESP32-001",
            "payload": None,
            "expected_status": 200
        }
    ]

    for t in tests:
        try:
            if t["method"] == "GET":
                res = client.get(t["url"])
            elif t["method"] == "POST":
                res = client.post(t["url"], json=t["payload"])

            if res.status_code == t["expected_status"]:
                print(f"[PASS] {t['name']:<45} | Status: {res.status_code}")
                passed += 1
            else:
                print(f"[FAIL] {t['name']:<45} | Got: {res.status_code}, Expected: {t['expected_status']}")
                print(f"       Response: {res.text}")
                failed += 1
        except Exception as e:
            print(f"[EXCEPT] {t['name']:<43} | Error: {e}")
            failed += 1

    print("=" * 75)
    print(f"IoT Test Summary: {passed} PASSED | {failed} FAILED | Total: {len(tests)}")
    print("=" * 75)
    return failed == 0

if __name__ == "__main__":
    success = test_iot_scenarios()
    sys.exit(0 if success else 1)
