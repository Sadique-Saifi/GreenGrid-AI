"""
GreenGrid AI — Energy Route Module
Endpoints for current telemetry, historical series, environment impact, and device status.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.energy_service import EnergyService
import models
import schemas

router = APIRouter(tags=["Energy & Devices"])

@router.get("/api/energy/current")
@router.get("/energy/current")
def get_current_energy(db: Session = Depends(get_db)):
    """Retrieves real-time power telemetry and weather snapshot."""
    return EnergyService.get_latest_telemetry(db)

@router.get("/api/energy/history")
@router.get("/energy/history")
def get_energy_history(days: int = Query(7, description="7, 14, or 30 days"), db: Session = Depends(get_db)):
    """Retrieves historical energy consumption vs. generation arrays."""
    return EnergyService.get_energy_history(db, days=days)

@router.get("/api/environment/impact")
@router.get("/environment/impact")
def get_environmental_impact(db: Session = Depends(get_db)):
    """Retrieves carbon offset and environmental sustainability metrics."""
    return EnergyService.get_environmental_impact(db)

@router.get("/api/devices")
@router.get("/devices")
def get_devices(db: Session = Depends(get_db)):
    """Retrieves list of registered microgrid devices with latest sensor readings."""
    devices = db.query(models.DeviceModel).all()
    result = []
    for d in devices:
        result.append(EnergyService.get_device_detail(db, d.device_id))
    return result

@router.get("/api/devices/{device_id}")
@router.get("/devices/{device_id}")
def get_device_by_id(device_id: str, db: Session = Depends(get_db)):
    """Retrieves metadata and latest sensor metrics for a specific device by ID."""
    return EnergyService.get_device_detail(db, device_id)
