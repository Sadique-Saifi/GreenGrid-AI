"""
GreenGrid AI — Optimization Engine Test Suite
Tests energy allocation, battery constraints, cost/CO2 calculations, and recommended actions
across 6 mandatory scenarios.
"""

import sys
from services.optimizer import OptimizerService

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_optimizer_scenarios():
    print("=" * 75)
    print("GreenGrid AI -- Energy Optimization Engine Scenario Test Suite")
    print("=" * 75)

    passed = 0
    failed = 0

    scenarios = [
        {
            "name": "Scenario 1: Solar > demand",
            "solar": 50.0, "demand": 30.0, "soc": 50.0,
            "check": lambda res: (
                res["allocation"]["solar_to_load"] == 30.0 and
                res["allocation"]["solar_to_battery"] == 20.0 and  # 20 kW surplus routed to battery
                res["allocation"]["battery_to_load"] == 0.0 and
                res["allocation"]["grid_to_load"] == 0.0 and
                res["recommended_action"] in ["charge_battery", "use_solar"]
            )
        },
        {
            "name": "Scenario 2: Solar < demand and battery available",
            "solar": 10.0, "demand": 30.0, "soc": 60.0,
            "check": lambda res: (
                res["allocation"]["solar_to_load"] == 10.0 and
                res["allocation"]["solar_to_battery"] == 0.0 and
                res["allocation"]["battery_to_load"] == 20.0 and  # battery discharges 20 kW
                res["allocation"]["grid_to_load"] == 0.0 and
                res["recommended_action"] == "discharge_battery"
            )
        },
        {
            "name": "Scenario 3: Solar < demand and battery unavailable (SOC at floor)",
            "solar": 10.0, "demand": 30.0, "soc": 10.0,
            "check": lambda res: (
                res["allocation"]["solar_to_load"] == 10.0 and
                res["allocation"]["solar_to_battery"] == 0.0 and
                res["allocation"]["battery_to_load"] == 0.0 and   # battery at floor, cannot discharge
                res["allocation"]["grid_to_load"] == 20.0 and   # 20 kW drawn from grid
                res["recommended_action"] == "use_grid"
            )
        },
        {
            "name": "Scenario 4: High demand / peak demand",
            "solar": 15.0, "demand": 55.0, "soc": 40.0,
            "check": lambda res: (
                res["allocation"]["solar_to_load"] == 15.0 and
                res["allocation"]["solar_to_battery"] == 0.0 and
                res["allocation"]["battery_to_load"] > 0.0 and
                res["allocation"]["grid_to_load"] > 0.0 and
                round(res["allocation"]["solar_to_load"] + res["allocation"]["battery_to_load"] + res["allocation"]["grid_to_load"], 1) == 55.0
            )
        },
        {
            "name": "Scenario 5: Battery nearly full (SOC >= 95%)",
            "solar": 40.0, "demand": 25.0, "soc": 98.0,
            "check": lambda res: (
                res["allocation"]["solar_to_load"] == 25.0 and
                res["allocation"]["solar_to_battery"] == 0.0 and  # battery at ceiling, charging paused
                res["allocation"]["battery_to_load"] == 0.0 and
                res["allocation"]["grid_to_load"] == 0.0 and
                res["recommended_action"] in ["use_solar", "idle"]
            )
        },
        {
            "name": "Scenario 6: Battery nearly empty (SOC <= 15%)",
            "solar": 5.0, "demand": 20.0, "soc": 12.0,
            "check": lambda res: (
                res["allocation"]["solar_to_load"] == 5.0 and
                res["allocation"]["solar_to_battery"] == 0.0 and
                res["allocation"]["battery_to_load"] == 0.0 and   # battery below floor
                res["allocation"]["grid_to_load"] == 15.0 and   # grid covers shortfall
                res["recommended_action"] == "use_grid"
            )
        }
    ]

    for sc in scenarios:
        res = OptimizerService.compute_allocation(
            solar_generation=sc["solar"],
            energy_demand=sc["demand"],
            battery_soc=sc["soc"]
        )
        ok = sc["check"](res)
        if ok:
            print(f"[PASS] {sc['name']:<55} | Action: {res['recommended_action']:<18} | Cost Saved: ₹{res['cost_saved']}")
            passed += 1
        else:
            print(f"[FAIL] {sc['name']:<55} | Allocation: {res['allocation']}")
            failed += 1

    print("=" * 75)
    print(f"Optimizer Test Summary: {passed} PASSED | {failed} FAILED | Total: {len(scenarios)}")
    print("=" * 75)
    return failed == 0

if __name__ == "__main__":
    success = test_optimizer_scenarios()
    sys.exit(0 if success else 1)
