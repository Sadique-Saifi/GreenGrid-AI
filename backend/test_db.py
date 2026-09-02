"""
GreenGrid AI — Database Connection Verification Script
Tests connectivity to Neon PostgreSQL without revealing sensitive credentials.
"""

import sys
from datetime import datetime, timezone
from sqlalchemy import text
from database import engine, SessionLocal
from models import DeviceModel, EnergyDataModel, BatteryDataModel, PredictionModel, OptimizationResultModel

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def test_connection():
    print("=" * 60)
    print("GreenGrid AI -- Testing Neon PostgreSQL Connection")
    print("=" * 60)

    try:
        db = SessionLocal()
        # Execute raw SQL query to test active connection and database version
        result = db.execute(text("SELECT version();")).fetchone()
        db_version = result[0] if result else "Unknown"

        print("[OK] Database Connection Successful!")
        print(f"     Provider: Neon PostgreSQL")
        print(f"     Postgres Version: {db_version.split(',')[0]}")
        print(f"     Verified At: {datetime.now(timezone.utc).isoformat()}")

        # Verify tables and row counts
        tables_to_check = [
            ("devices", DeviceModel),
            ("energy_data", EnergyDataModel),
            ("battery_data", BatteryDataModel),
            ("predictions", PredictionModel),
            ("optimization_results", OptimizationResultModel),
        ]

        print("\n--- Verified Tables & Record Counts ---")
        for table_name, model in tables_to_check:
            count = db.query(model).count()
            print(f"   * Table '{table_name}': {count} rows")

        db.close()
        print("=" * 60)
        return True

    except Exception as e:
        print(f"[ERROR] Connection test failed: {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
