"""
GreenGrid AI — Configuration Route Module
Endpoints for site capacity parameters and operational system control toggles.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(tags=["Site Configuration & Controls"])

# In-memory configuration store fallback (persisted in session)
DEFAULT_CONFIG = {
    "solar_capacity": 50.0,
    "battery_capacity": 100.0,
    "avg_daily_demand": 350.0,
    "battery_soc_ceiling": 95.0,
    "battery_soc_floor": 15.0,
    "auto_optimize": True,
    "peak_alerts": True,
    "grid_export": False,
    "simulation_mode": False,
}

class SiteConfigPayload(BaseModel):
    solar_capacity: Optional[float] = Field(50.0, ge=0.0, description="Installed solar capacity in kW")
    battery_capacity: Optional[float] = Field(100.0, ge=0.0, description="Battery capacity in kWh")
    avg_daily_demand: Optional[float] = Field(350.0, ge=0.0, description="Average daily demand in kWh")
    battery_soc_ceiling: Optional[float] = Field(95.0, ge=50.0, le=100.0, description="SOC upper safety ceiling %")
    battery_soc_floor: Optional[float] = Field(15.0, ge=0.0, le=50.0, description="SOC lower safety floor %")
    auto_optimize: Optional[bool] = Field(True, description="Enable automatic AI optimization")
    peak_alerts: Optional[bool] = Field(True, description="Enable peak demand alerts")
    grid_export: Optional[bool] = Field(False, description="Allow surplus export to grid")
    simulation_mode: Optional[bool] = Field(False, description="10x accelerated simulation mode")

@router.get("/api/config")
@router.get("/config")
def get_site_config(db: Session = Depends(get_db)):
    """Retrieves current site parameters, thresholds, and operational toggles."""
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    res = {**DEFAULT_CONFIG}
    res["timestamp"] = now_iso
    res["simulation_speed"] = "10x (accelerated)" if res.get("simulation_mode") else "1x (real-time)"
    return res

@router.post("/api/config")
@router.post("/config")
def update_site_config(payload: SiteConfigPayload, db: Session = Depends(get_db)):
    """Updates site parameters, thresholds, and operational toggles."""
    now_iso = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        if v is not None:
            DEFAULT_CONFIG[k] = v

    res = {**DEFAULT_CONFIG}
    res["timestamp"] = now_iso
    res["simulation_speed"] = "10x (accelerated)" if res.get("simulation_mode") else "1x (real-time)"
    return res
