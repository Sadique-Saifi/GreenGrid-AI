"""
GreenGrid AI — Dashboard Route Module
Endpoints for dashboard overview and KPI metrics.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.energy_service import EnergyService

router = APIRouter(tags=["Dashboard"])

@router.get("/api/dashboard/summary")
@router.get("/dashboard/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Retrieves cumulative KPI summary metrics for the dashboard."""
    return EnergyService.get_dashboard_summary(db)
