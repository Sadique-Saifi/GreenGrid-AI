from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

# ============================================================
# Device Schemas
# ============================================================
class DeviceBase(BaseModel):
    device_id: str = Field(..., example="ESP32-001")
    device_name: str = Field(..., example="ESP32 Solar Telemetry Controller")
    device_type: str = Field(default="ESP32_DEVKIT", example="ESP32_DEVKIT")
    location: str = Field(default="Delhi Campus Lab", example="Delhi Campus Lab")
    status: str = Field(default="online", example="online")  # online, offline, warning

class DeviceCreate(DeviceBase):
    pass

class DeviceResponse(DeviceBase):
    id: int
    device_status: str = Field(default="online", example="online")
    last_seen: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class DeviceDetailResponse(DeviceResponse):
    latest_temperature: Optional[float] = Field(None, example=32.5)
    latest_humidity: Optional[float] = Field(None, example=61.0)
    latest_light_intensity: Optional[float] = Field(None, example=785.0)
    latest_voltage: Optional[float] = Field(None, example=12.1)
    latest_current: Optional[float] = Field(None, example=1.8)
    latest_power: Optional[float] = Field(None, example=21.78)


# ============================================================
# IoT Telemetry Validation Schemas
# ============================================================
class IoTTelemetryCreate(BaseModel):
    device_id: str = Field(..., description="Registered hardware device ID", example="ESP32-001")
    timestamp: datetime = Field(..., description="ISO 8601 UTC timestamp", example="2026-08-22T14:30:00Z")
    temperature: float = Field(..., ge=-40.0, le=85.0, description="Temperature in °C from DHT22/DHT11", example=32.5)
    humidity: float = Field(..., ge=0.0, le=100.0, description="Humidity percentage from DHT22/DHT11", example=61.0)
    light_intensity: float = Field(..., ge=0.0, description="Relative LDR light intensity reading", example=785.0)
    voltage: float = Field(..., ge=0.0, description="Measured DC voltage in V from INA219", example=12.1)
    current: float = Field(..., ge=0.0, description="Measured DC current in A from INA219", example=1.8)
    power: Optional[float] = Field(None, ge=0.0, description="Electrical power in W (derived: voltage * current)", example=21.78)


# ============================================================
# Energy Data Schemas
# ============================================================
class EnergyDataBase(BaseModel):
    device_id: str = Field(default="DELHI_CAMPUS_01", example="DELHI_CAMPUS_01")
    timestamp: datetime
    solar_generation: float = Field(..., ge=0.0, description="Solar power generation in kW", example=42.0)
    energy_demand: float = Field(..., ge=0.0, description="Energy demand load in kW", example=31.0)
    temperature: Optional[float] = Field(None, description="Ambient temperature in °C", example=32.4)
    humidity: Optional[float] = Field(None, description="Humidity percentage", example=65.0)
    solar_radiation: Optional[float] = Field(None, description="Solar irradiance in W/m²", example=750.0)
    cloud_cover: Optional[float] = Field(None, description="Cloud cover percentage", example=20.0)
    grid_power: float = Field(default=0.0, ge=0.0, description="Grid power draw in kW", example=0.0)

class EnergyDataCreate(EnergyDataBase):
    pass

class EnergyDataResponse(EnergyDataBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# Battery Data Schemas
# ============================================================
class BatteryDataBase(BaseModel):
    device_id: str = Field(default="DELHI_CAMPUS_01", example="DELHI_CAMPUS_01")
    timestamp: datetime
    battery_soc: float = Field(..., ge=0.0, le=100.0, description="Battery SOC %", example=66.0)
    battery_power: float = Field(default=0.0, description="Battery power in kW (+ charge, - discharge)", example=11.0)
    battery_capacity: float = Field(default=100.0, gt=0.0, description="Battery capacity in kWh", example=100.0)
    battery_status: str = Field(default="CHARGING", description="CHARGING, DISCHARGING, IDLE", example="CHARGING")

class BatteryDataCreate(BatteryDataBase):
    pass

class BatteryDataResponse(BatteryDataBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# Prediction Schemas
# ============================================================
class PredictionBase(BaseModel):
    timestamp: datetime
    predicted_demand: float = Field(..., ge=0.0, description="Forecasted demand in kW", example=4.2)
    predicted_solar_generation: float = Field(..., ge=0.0, description="Forecasted solar in kW", example=3.1)
    model_version: str = Field(default="v1.0.0", example="v1.0.0")

class PredictionCreate(PredictionBase):
    pass

class PredictionResponse(PredictionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# Optimization Result Schemas
# ============================================================
class OptimizationResultBase(BaseModel):
    timestamp: datetime
    solar_to_load: float = Field(default=0.0, ge=0.0, example=31.0)
    solar_to_battery: float = Field(default=0.0, ge=0.0, example=11.0)
    battery_to_load: float = Field(default=0.0, ge=0.0, example=0.0)
    grid_to_load: float = Field(default=0.0, ge=0.0, example=0.0)
    recommended_action: str = Field(..., example="charge_battery")
    reason: str = Field(..., example="Solar output (42 kW) exceeds demand (31 kW) -- surplus routed to battery.")
    energy_saved: float = Field(default=0.0, ge=0.0, description="Energy saved in kWh", example=14.5)
    cost_saved: float = Field(default=0.0, ge=0.0, description="Cost saved in INR", example=210.0)
    co2_avoided: float = Field(default=0.0, ge=0.0, description="CO2 avoided in kg", example=14.2)

class OptimizationResultCreate(OptimizationResultBase):
    pass

class OptimizationResultResponse(OptimizationResultBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# Simulator API Schemas
# ============================================================
class SimulatorInput(BaseModel):
    solar_generation: float = Field(..., ge=0.0, le=100.0, example=42.0)
    energy_demand: float = Field(..., ge=0.0, le=100.0, example=31.0)
    battery_soc: float = Field(..., ge=0.0, le=100.0, example=66.0)

class SimulatorAllocation(BaseModel):
    solar_to_load: float
    solar_to_battery: float
    battery_to_load: float
    grid_to_load: float

class SimulatorMetrics(BaseModel):
    cost_saved: float
    co2_avoided: float

class SimulatorOutput(BaseModel):
    timestamp: datetime
    input: SimulatorInput
    allocation: SimulatorAllocation
    metrics: SimulatorMetrics
    recommended_action: str
    reason: str


# ============================================================
# Health Check & Status Schemas
# ============================================================
class DatabaseHealthResponse(BaseModel):
    status: str = Field(..., example="connected")
    database_type: str = Field(..., example="Neon PostgreSQL")
    tables_verified: List[str]
    timestamp: datetime
