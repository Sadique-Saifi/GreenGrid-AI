"""
GreenGrid AI — Battery Route Module
Endpoints for battery status and BMS monitoring.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.energy_service import EnergyService

router = APIRouter(tags=["Battery"])

@router.get("/api/battery/status")
@router.get("/battery/status")
def get_battery_status(db: Session = Depends(get_db)):
    """Retrieves current battery state-of-charge and charge/discharge status."""
    latest = EnergyService.get_latest_telemetry(db)
    soc = latest["battery_soc"]
    power = latest["battery_power"]

    return {
        "timestamp": latest["timestamp"],
        "device_id": latest["device_id"],
        "battery_soc": soc,
        "soc": soc,  # Legacy alias
        "battery_power": power,
        "charging_rate": max(0.0, power),
        "discharging_rate": abs(min(0.0, power)),
        "battery_capacity": 100.0,
        "battery_status": "CHARGING" if power >= 0 else "DISCHARGING"
    }
