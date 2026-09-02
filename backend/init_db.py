"""
GreenGrid AI — Database Initialization & Migration Script
Connects to Neon PostgreSQL and creates all required schema tables.
"""

import sys
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import DeviceModel, IoTReadingModel, EnergyDataModel, BatteryDataModel, PredictionModel, OptimizationResultModel

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def init_database():
    print("=" * 60)
    print("GreenGrid AI -- PostgreSQL Database Initialization")
    print("=" * 60)

    try:
        print("[1/3] Creating database tables in Neon PostgreSQL...")
        Base.metadata.create_all(bind=engine)
        print("      [OK] All 6 tables created successfully (devices, iot_readings, energy_data, battery_data, predictions, optimization_results).")

        print("[2/3] Verifying and seeding registered device metadata...")
        db: Session = SessionLocal()
        try:
            # Seed DELHI_CAMPUS_01
            d1 = db.query(DeviceModel).filter(DeviceModel.device_id == "DELHI_CAMPUS_01").first()
            if not d1:
                d1 = DeviceModel(
                    device_id="DELHI_CAMPUS_01",
                    device_name="Delhi Campus Microgrid Controller",
                    device_type="MICROGRID_CONTROLLER",
                    location="Delhi Campus Main",
                    status="online",
                    last_seen=datetime.now(timezone.utc)
                )
                db.add(d1)
                print("      [OK] Initial device record 'DELHI_CAMPUS_01' created.")

            # Seed ESP32-001
            d2 = db.query(DeviceModel).filter(DeviceModel.device_id == "ESP32-001").first()
            if not d2:
                d2 = DeviceModel(
                    device_id="ESP32-001",
                    device_name="ESP32 Solar Telemetry Unit",
                    device_type="ESP32_DEVKIT",
                    location="Delhi Campus Lab Roof",
                    status="online",
                    last_seen=datetime.now(timezone.utc)
                )
                db.add(d2)
                print("      [OK] Initial device record 'ESP32-001' created.")

            db.commit()
        finally:
            db.close()

        print("[3/3] Database initialization completed cleanly.")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"[ERROR] Database initialization failed: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
