"""
GreenGrid AI — IoT Data Ingestion Route Module
Endpoints for receiving hardware telemetry packets from ESP32 microcontrollers over Wi-Fi.
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.energy_service import EnergyService
import schemas

router = APIRouter(tags=["IoT Telemetry Ingestion"])

@router.post("/api/iot/energy", status_code=status.HTTP_201_CREATED)
@router.post("/api/energy/data", status_code=status.HTTP_201_CREATED)
@router.post("/energy/data", status_code=status.HTTP_201_CREATED)
def ingest_iot_energy(payload: dict, db: Session = Depends(get_db)):
    """
    Receives physical ESP32 telemetry packet over Wi-Fi and persists into Neon PostgreSQL.
    Validates device registration, timestamp, temperature, humidity, voltage, and current bounds.
    """
    iot_record = EnergyService.validate_and_ingest_iot_telemetry(db, payload)
    return {
        "status": "success",
        "message": "Telemetry received and ingested into database",
        "ingested_id": iot_record.id,
        "device_id": iot_record.device_id,
        "timestamp": iot_record.timestamp.isoformat().replace("+00:00", "Z")
    }
