"""
GreenGrid AI — Optimization Route Module
Endpoints for AI energy allocation recommendations and what-if scenario simulations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.energy_service import EnergyService
from services.optimizer import OptimizerService
import schemas

router = APIRouter(tags=["Optimization & Simulator"])

@router.get("/api/optimization/recommendation")
@router.get("/optimization/recommendation")
def get_optimization_recommendation(db: Session = Depends(get_db)):
    """Retrieves current AI energy allocation decision, reasoning, and recommendations."""
    latest = EnergyService.get_latest_telemetry(db)
    return OptimizerService.compute_allocation(
        solar=latest["solar_generation"],
        demand=latest["energy_demand"],
        battery_soc=latest["battery_soc"]
    )

@router.post("/api/optimization/simulate")
@router.post("/api/simulator/run")
@router.post("/simulator/run")
def run_simulation(payload: schemas.SimulatorInput):
    """Calculates allocation decision and savings metrics for custom simulated inputs."""
    return OptimizerService.compute_allocation(
        solar=payload.solar_generation,
        demand=payload.energy_demand,
        battery_soc=payload.battery_soc
    )
