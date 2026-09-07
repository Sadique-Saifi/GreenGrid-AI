


"""
GreenGrid AI — Demand Model Training Script
Trains a Random Forest Regressor to predict electricity demand (energy_demand).
Saves trained model artifact to ML/models/demand_model.pkl.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from preprocessing import prepare_demand_datasets, DEMAND_FEATURES

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")

def train_demand_model(models_dir: str = DEFAULT_MODELS_DIR):
    print("=" * 60)
    print("GreenGrid AI -- Training Electricity Demand Model (energy_demand)")
    print("=" * 60)

    X_train, y_train, X_val, y_val, X_test, y_test = prepare_demand_datasets()
    print(f"Data Split Sizes: Train={len(X_train)} | Val={len(X_val)} | Test={len(X_test)}")
    print(f"Features ({len(DEMAND_FEATURES)}): {DEMAND_FEATURES}\n")

    # Initialize Random Forest Regressor
    model = RandomForestRegressor(
        n_estimators=150,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )

    print("Training Random Forest Regressor...")
    model.fit(X_train, y_train)

    # Evaluate on Train, Validation, and Test splits
    def calculate_metrics(X, y):
        preds = model.predict(X)
        mae = mean_absolute_error(y, preds)
        rmse = np.sqrt(mean_squared_error(y, preds))
        r2 = r2_score(y, preds)
        return round(mae, 4), round(rmse, 4), round(r2, 4)

    tr_mae, tr_rmse, tr_r2 = calculate_metrics(X_train, y_train)
    val_mae, val_rmse, val_r2 = calculate_metrics(X_val, y_val)
    tst_mae, tst_rmse, tst_r2 = calculate_metrics(X_test, y_test)

    print("\n--- Evaluation Results ---")
    print(f"Train Set      | MAE: {tr_mae:.4f} kW | RMSE: {tr_rmse:.4f} kW | R2: {tr_r2:.4f}")
    print(f"Validation Set | MAE: {val_mae:.4f} kW | RMSE: {val_rmse:.4f} kW | R2: {val_r2:.4f}")
    print(f"Test Set       | MAE: {tst_mae:.4f} kW | RMSE: {tst_rmse:.4f} kW | R2: {tst_r2:.4f}")

    # Ensure models directory exists
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "demand_model.pkl")

    # Package model artifact with feature metadata
    artifact = {
        "model": model,
        "features": DEMAND_FEATURES,
        "target": "energy_demand",
        "model_type": "RandomForestRegressor",
        "version": "1.0.0",
        "metrics": {
            "test_mae": tst_mae,
            "test_rmse": tst_rmse,
            "test_r2": tst_r2
        }
    }

    joblib.dump(artifact, model_path)
    print(f"\n[OK] Demand model saved successfully to: {model_path}")
    print("=" * 60)
    return artifact

if __name__ == "__main__":
    train_demand_model()
