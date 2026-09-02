from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from database import Base

class DeviceModel(Base):
    """
    Devices Table — Stores registered microgrid hardware devices and controllers.
    """
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), unique=True, nullable=False, index=True)
    device_name = Column(String(100), nullable=False)
    device_type = Column(String(50), nullable=False, default="ESP32_DEVKIT")
    location = Column(String(100), nullable=False, default="Delhi Campus Lab")
    status = Column(String(50), nullable=False, default="online")  # online, offline, warning
    last_seen = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=True)

    # Relationships
    energy_readings = relationship("EnergyDataModel", back_populates="device", cascade="all, delete-orphan")
    battery_readings = relationship("BatteryDataModel", back_populates="device", cascade="all, delete-orphan")
    iot_readings = relationship("IoTReadingModel", back_populates="device", cascade="all, delete-orphan")


class IoTReadingModel(Base):
    """
    IoT Readings Table — Stores raw telemetry signals received from physical ESP32 sensors
    (DHT22 temp/humidity, LDR light_intensity, INA219 voltage/current/power).
    """
    __tablename__ = "iot_readings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey("devices.device_id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    temperature = Column(Float, nullable=False)                        # °C (from DHT22/DHT11)
    humidity = Column(Float, nullable=False)                           # % (from DHT22/DHT11)
    light_intensity = Column(Float, nullable=False)                    # Raw LDR light intensity
    voltage = Column(Float, nullable=False)                            # V (from INA219)
    current = Column(Float, nullable=False)                            # A (from INA219)
    power = Column(Float, nullable=False)                              # W (voltage * current)
    estimated_solar_generation = Column(Float, nullable=True)         # kW (derived estimate)

    # Relationship
    device = relationship("DeviceModel", back_populates="iot_readings")

    __table_args__ = (
        Index("idx_iot_device_timestamp", "device_id", "timestamp"),
    )


class EnergyDataModel(Base):
    """
    Energy Data Table — Stores historical and live power telemetry & weather features.
    """
    __tablename__ = "energy_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey("devices.device_id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    solar_generation = Column(Float, nullable=False, default=0.0)  # kW
    energy_demand = Column(Float, nullable=False, default=0.0)     # kW
    temperature = Column(Float, nullable=True)                      # °C
    humidity = Column(Float, nullable=True)                         # %
    solar_radiation = Column(Float, nullable=True)                  # W/m²
    cloud_cover = Column(Float, nullable=True)                      # %
    grid_power = Column(Float, nullable=False, default=0.0)         # kW

    # Relationship
    device = relationship("DeviceModel", back_populates="energy_readings")

    __table_args__ = (
        Index("idx_energy_device_timestamp", "device_id", "timestamp"),
    )


class BatteryDataModel(Base):
    """
    Battery Data Table — Stores battery state of charge and power flow metrics.
    """
    __tablename__ = "battery_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(50), ForeignKey("devices.device_id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    battery_soc = Column(Float, nullable=False)                     # %
    battery_power = Column(Float, nullable=False, default=0.0)      # kW (+ charge, - discharge)
    battery_capacity = Column(Float, nullable=False, default=100.0)  # kWh
    battery_status = Column(String(50), nullable=False, default="CHARGING") # CHARGING, DISCHARGING, IDLE

    # Relationship
    device = relationship("DeviceModel", back_populates="battery_readings")

    __table_args__ = (
        Index("idx_battery_device_timestamp", "device_id", "timestamp"),
    )


class PredictionModel(Base):
    """
    Predictions Table — Stores ML model forecast outputs for demand and solar generation.
    """
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    predicted_demand = Column(Float, nullable=False)               # kW
    predicted_solar_generation = Column(Float, nullable=False)     # kW
    model_version = Column(String(50), nullable=False, default="v1.0.0")

    __table_args__ = (
        Index("idx_predictions_timestamp", "timestamp"),
    )


class OptimizationResultModel(Base):
    """
    Optimization Results Table — Stores optimizer energy allocation decisions & reasoning.
    """
    __tablename__ = "optimization_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    solar_to_load = Column(Float, nullable=False, default=0.0)     # kW
    solar_to_battery = Column(Float, nullable=False, default=0.0)  # kW
    battery_to_load = Column(Float, nullable=False, default=0.0)  # kW
    grid_to_load = Column(Float, nullable=False, default=0.0)     # kW
    recommended_action = Column(String(50), nullable=False)       # Enum string
    reason = Column(Text, nullable=False)                          # Explainability text
    energy_saved = Column(Float, nullable=False, default=0.0)     # kWh
    cost_saved = Column(Float, nullable=False, default=0.0)       # INR (₹)
    co2_avoided = Column(Float, nullable=False, default=0.0)       # kg

    __table_args__ = (
        Index("idx_optimization_timestamp", "timestamp"),
    )
