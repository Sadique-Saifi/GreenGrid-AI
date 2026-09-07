"""
GreenGrid AI — Model Evaluation & Validation Script
Loads saved .pkl model artifacts from ML/models/ and validates Test set performance.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from preprocessing import prepare_demand_datasets, prepare_solar_datasets

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def evaluate_models(models_dir: str = "ML/models"):
    print("=" * 65)
    print("GreenGrid AI -- Evaluation & Verification of Saved ML Models")
    print("=" * 65)

    demand_path = os.path.join(models_dir, "demand_model.pkl")
    solar_path = os.path.join(models_dir, "solar_model.pkl")

    if not os.path.exists(demand_path) or not os.path.exists(solar_path):
        print("[ERROR] Model files missing! Please run train_demand.py and train_solar.py first.")
        return False

    # 1. Evaluate Demand Model
    print("\n--- 1. Demand Model Evaluation (demand_model.pkl) ---")
    demand_artifact = joblib.load(demand_path)
    demand_model = demand_artifact["model"]
    _, _, _, _, X_test_dem, y_test_dem = prepare_demand_datasets()

    preds_dem = demand_model.predict(X_test_dem)
    dem_mae = mean_absolute_error(y_test_dem, preds_dem)
    dem_rmse = np.sqrt(mean_squared_error(y_test_dem, preds_dem))
    dem_r2 = r2_score(y_test_dem, preds_dem)

    print(f"Model Type   : {demand_artifact.get('model_type', 'RandomForestRegressor')}")
    print(f"Target       : {demand_artifact.get('target')}")
    print(f"Features ({len(demand_artifact['features'])}): {demand_artifact['features']}")
    print(f"Test Set MAE : {dem_mae:.4f} kW")
    print(f"Test Set RMSE: {dem_rmse:.4f} kW")
    print(f"Test Set R²  : {dem_r2:.4f}")

    # 2. Evaluate Solar Model
    print("\n--- 2. Solar Model Evaluation (solar_model.pkl) ---")
    solar_artifact = joblib.load(solar_path)
    solar_model = solar_artifact["model"]
    _, _, _, _, X_test_sol, y_test_sol = prepare_solar_datasets()

    preds_sol = solar_model.predict(X_test_sol)
    sol_mae = mean_absolute_error(y_test_sol, preds_sol)
    sol_rmse = np.sqrt(mean_squared_error(y_test_sol, preds_sol))
    sol_r2 = r2_score(y_test_sol, preds_sol)

    print(f"Model Type   : {solar_artifact.get('model_type', 'RandomForestRegressor')}")
    print(f"Target       : {solar_artifact.get('target')}")
    print(f"Features ({len(solar_artifact['features'])}): {solar_artifact['features']}")
    print(f"Test Set MAE : {sol_mae:.4f} kW")
    print(f"Test Set RMSE: {sol_rmse:.4f} kW")
    print(f"Test Set R²  : {sol_r2:.4f}")

    print("\n[OK] Model evaluation completed successfully.")
    print("=" * 65)
    return True

if __name__ == "__main__":
    success = evaluate_models()
    sys.exit(0 if success else 1)
