"""
GreenGrid AI — Comprehensive API Endpoint Test Suite
Tests all 16 endpoints against FastAPI app using TestClient.
"""

import sys
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from main import app

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

client = TestClient(app)

def run_all_tests():
    print("=" * 70)
    print("GreenGrid AI -- API Endpoint Automated Test Suite")
    print("=" * 70)

    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    tests = [
        ("Database Health", "GET", "/health/db", None, 200),
        ("Dashboard Summary", "GET", "/api/dashboard/summary", None, 200),
        ("Current Energy", "GET", "/api/energy/current", None, 200),
        ("Energy History (7d)", "GET", "/api/energy/history?days=7", None, 200),
        ("Energy History (30d)", "GET", "/api/energy/history?days=30", None, 200),
        ("Forecast (6h)", "GET", "/api/forecast?hours=6", None, 200),
        ("Forecast Demand", "GET", "/api/forecast/demand", None, 200),
        ("Forecast Solar", "GET", "/api/forecast/solar", None, 200),
        ("Battery Status", "GET", "/api/battery/status", None, 200),
        ("Optimization Rec", "GET", "/api/optimization/recommendation", None, 200),
        ("Optimization Simulate", "POST", "/api/optimization/simulate", {"solar_generation": 45.0, "energy_demand": 30.0, "battery_soc": 70.0}, 200),
        ("Environmental Impact", "GET", "/api/environment/impact", None, 200),
        ("Devices List", "GET", "/api/devices", None, 200),
        ("Device Detail", "GET", "/api/devices/DELHI_CAMPUS_01", None, 200),
        ("IoT Energy Ingest", "POST", "/api/iot/energy", {
            "device_id": "ESP32-001",
            "timestamp": now_iso,
            "temperature": 32.4,
            "humidity": 65.0,
            "light_intensity": 750.0,
            "voltage": 12.1,
            "current": 1.8,
            "power": 21.78
        }, 201),
        ("Model Health", "GET", "/api/model/health", None, 200),
        ("Site Config GET", "GET", "/api/config", None, 200),
        ("Site Config POST", "POST", "/api/config", {"solar_capacity": 55.0, "battery_capacity": 120.0}, 200)
    ]

    passed = 0
    failed = 0

    for name, method, url, payload, expected_status in tests:
        try:
            if method == "GET":
                res = client.get(url)
            elif method == "POST":
                res = client.post(url, json=payload)

            if res.status_code == expected_status:
                print(f"[PASS] {name:<25} | {method} {url:<32} | Status: {res.status_code}")
                passed += 1
            else:
                print(f"[FAIL] {name:<25} | {method} {url:<32} | Got: {res.status_code}, Expected: {expected_status}")
                print(f"       Response: {res.text}")
                failed += 1
        except Exception as e:
            print(f"[EXCEPT] {name:<23} | {method} {url:<32} | Error: {e}")
            failed += 1

    print("=" * 70)
    print(f"Test Summary: {passed} PASSED | {failed} FAILED | Total: {len(tests)}")
    print("=" * 70)
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
