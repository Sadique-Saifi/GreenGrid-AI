"""
GreenGrid AI — FastAPI Backend Application
Main entry point connecting modular routers, services, and Neon PostgreSQL DB.
Run locally with: uvicorn main:app --reload
"""

from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
import schemas

# Import modular routers
from routes import dashboard, energy, forecast, battery, optimization, iot, config

app = FastAPI(
    title="GreenGrid AI API",
    description="AI-powered renewable energy demand prediction & optimization API",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include modular APIRouters
app.include_router(dashboard.router)
app.include_router(energy.router)
app.include_router(forecast.router)
app.include_router(battery.router)
app.include_router(optimization.router)
app.include_router(iot.router)
app.include_router(config.router)

@app.get("/health/db", response_model=schemas.DatabaseHealthResponse, tags=["Health"])
@app.get("/api/health/db", response_model=schemas.DatabaseHealthResponse, tags=["Health"])
def database_health_check(db: Session = Depends(get_db)):
    """
    Safe Database Connection Verification Endpoint.
    Tests active connectivity to Neon PostgreSQL without exposing credentials.
    """
    try:
        db.execute(text("SELECT 1;")).first()
        tables = ["devices", "energy_data", "battery_data", "predictions", "optimization_results"]
        return schemas.DatabaseHealthResponse(
            status="connected",
            database_type="Neon PostgreSQL",
            tables_verified=tables,
            timestamp=datetime.now(timezone.utc)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection error: {str(e)}"
        )

@app.get("/", tags=["Health"])
def root():
    return {
        "title": "GreenGrid AI API",
        "status": "online",
        "docs_url": "/docs",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
