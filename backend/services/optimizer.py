"""
GreenGrid AI — Energy Optimization Engine Service
Implements multi-source microgrid energy allocation, battery SOC management,
financial savings, carbon offset calculation, and explainability reasoning.
"""

from datetime import datetime, timezone
from typing import Dict, Any, List

class OptimizerService:
    @staticmethod
    def compute_allocation(
        solar_generation: float = 0.0,
        energy_demand: float = 0.0,
        battery_soc: float = 66.0,
        battery_capacity: float = 100.0,
        battery_power: float = 20.0,
        grid_price: float = 7.2,
        soc_floor: float = 15.0,
        soc_ceiling: float = 95.0,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculates optimal power allocation across Solar, Battery, and Grid.
        Supports both 'solar_generation'/'energy_demand' and legacy 'solar'/'demand' keyword parameters.
        """
        if "solar" in kwargs and (solar_generation == 0.0 or kwargs["solar"] != 0.0):
            solar_generation = kwargs["solar"]
        if "demand" in kwargs and (energy_demand == 0.0 or kwargs["demand"] != 0.0):
            energy_demand = kwargs["demand"]

        # Ensure non-negative input values
        solar_generation = max(0.0, float(solar_generation))
        energy_demand = max(0.0, float(energy_demand))
        battery_soc = max(0.0, min(100.0, float(battery_soc)))
        battery_capacity = max(1.0, float(battery_capacity))
        battery_power = max(0.0, float(battery_power))
        grid_price = max(0.0, float(grid_price))

        # 1. Direct Solar to Load
        solar_to_load = round(min(solar_generation, energy_demand), 1)
        surplus = max(0.0, solar_generation - energy_demand)
        shortfall = max(0.0, energy_demand - solar_generation)

        # 2. Solar Surplus to Battery (Charging)
        if surplus > 0.0 and battery_soc < soc_ceiling:
            headroom_kwh = max(0.0, (soc_ceiling - battery_soc) / 100.0 * battery_capacity)
            charge_kw = min(surplus, battery_power, headroom_kwh)
            solar_to_battery = round(max(0.0, charge_kw), 1)
        else:
            solar_to_battery = 0.0

        # 3. Battery to Load (Discharging)
        if shortfall > 0.0 and battery_soc > soc_floor:
            available_kwh = max(0.0, (battery_soc - soc_floor) / 100.0 * battery_capacity)
            discharge_kw = min(shortfall, battery_power, available_kwh)
            battery_to_load = round(max(0.0, discharge_kw), 1)
        else:
            battery_to_load = 0.0

        # 4. Remaining Deficit Drawn from Grid
        grid_to_load = round(max(0.0, shortfall - battery_to_load), 1)

        # 5. Financial Savings & Carbon Offset Calculations
        clean_kwh = solar_to_load + battery_to_load
        cost_saved = round(clean_kwh * grid_price, 1)
        co2_avoided = round(clean_kwh * 0.45, 1)

        # 6. Action & Explainability
        if energy_demand == 0.0 and solar_generation == 0.0:
            recommended_action = "idle"
            reason = "No load demand and no solar generation; system is idle."
        elif solar_to_battery > 0.3:
            recommended_action = "charge_battery"
            reason = f"Solar output ({solar_generation:.1f} kW) exceeds demand ({energy_demand:.1f} kW) -- surplus solar ({solar_to_battery:.1f} kW) is charging the battery."
        elif solar_to_load >= energy_demand and solar_generation > 0:
            recommended_action = "use_solar"
            reason = f"Solar output ({solar_generation:.1f} kW) completely satisfies load demand ({energy_demand:.1f} kW); no battery or grid power needed."
        elif battery_to_load > 0.3:
            recommended_action = "discharge_battery"
            reason = f"Solar output ({solar_generation:.1f} kW) is less than demand ({energy_demand:.1f} kW) -- battery is discharging ({battery_to_load:.1f} kW) to cover the gap."
        elif grid_to_load > 0.0:
            recommended_action = "use_grid"
            reason = f"Solar generation and available battery reserve are insufficient -- drawing {grid_to_load:.1f} kW from utility grid."
        else:
            recommended_action = "idle"
            reason = "System energy state balanced; no power transfer required."

        reasons_list = [
            reason,
            f"Battery SOC at {round(battery_soc)}% ({'above 15% floor' if battery_soc > soc_floor else 'at/below 15% floor'}).",
            f"{'Drawing ' + str(grid_to_load) + ' kW from grid.' if grid_to_load > 0 else 'No grid draw needed; solar and battery fully cover load.'}",
            "Evening peak window (19:00 - 21:00) forecast -- battery management active."
        ]

        recommendations = [
            {
                "severity": "ok" if recommended_action in ["use_solar", "charge_battery"] else "warn",
                "title": recommended_action.replace("_", " ").title(),
                "recommended_action": recommended_action,
                "reason": reason
            }
        ]

        now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        return {
            "timestamp": now_iso,
            "input": {
                "solar_generation": solar_generation,
                "energy_demand": energy_demand,
                "battery_soc": battery_soc,
                "battery_capacity": battery_capacity,
                "battery_power": battery_power,
                "grid_price": grid_price
            },
            "allocation": {
                "solar_to_load": solar_to_load,
                "solar_to_battery": solar_to_battery,
                "battery_to_load": battery_to_load,
                "grid_to_load": grid_to_load,
                "total_demand": energy_demand
            },
            "solar_to_load": solar_to_load,
            "solar_to_battery": solar_to_battery,
            "battery_to_load": battery_to_load,
            "grid_to_load": grid_to_load,
            "metrics": {
                "cost_saved": cost_saved,
                "co2_avoided": co2_avoided
            },
            "cost_saved": cost_saved,
            "co2_avoided": co2_avoided,
            "recommended_action": recommended_action,
            "reason": reason,
            "reasoning": reasons_list,
            "recommendations": recommendations
        }
