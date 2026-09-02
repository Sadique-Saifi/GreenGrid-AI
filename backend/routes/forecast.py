"""
GreenGrid AI — Forecast Route Module
Endpoints for multi-horizon ML load and solar predictions.
"""

from fastapi import APIRouter, Query
from services.ml_service import MLService

router = APIRouter(tags=["Forecast & ML"])

@router.get("/api/forecast")
@router.get("/forecast")
def get_forecast(hours: int = Query(6, description="6, 12, or 24 hours")):
    """Retrieves multi-horizon load demand and solar generation predictions."""
    return MLService.generate_forecast(hours=hours)

@router.get("/api/forecast/demand")
@router.get("/forecast/demand")
def forecast_demand():
    """Returns next hour and next 3 hours predicted demand load."""
    forecast = MLService.generate_forecast(hours=6)
    return {
        "next_hour": forecast["summary"]["next_hour_predicted_demand"],
        "next_3_hours": forecast["summary"]["next_3_hours_predicted_demand"],
        "peak_time": forecast["summary"]["predicted_peak_window"]
    }

@router.get("/api/forecast/solar")
@router.get("/forecast/solar")
def forecast_solar():
    """Returns next hour and next 3 hours predicted solar generation."""
    forecast = MLService.generate_forecast(hours=6)
    return {
        "next_hour": forecast["summary"]["next_hour_predicted_solar_generation"],
        "next_3_hours": round(sum(forecast["predicted_solar_generation"][:3]), 1)
    }

@router.get("/api/model/health")
@router.get("/model/health")
def get_model_health():
    """Retrieves current evaluation health metrics for deployed ML models."""
    return MLService.get_model_health()
