"""
GreenGrid AI — Inference Prediction Helper Script
Loads saved .pkl artifacts and generates predictions for given input features.
"""

import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List

class GreenGridPredictor:
    def __init__(self, models_dir: str = "ML/models"):
        demand_path = os.path.join(models_dir, "demand_model.pkl")
        solar_path = os.path.join(models_dir, "solar_model.pkl")

        if not os.path.exists(demand_path) or not os.path.exists(solar_path):
            # Check relative path fallback
            alt_models_dir = os.path.join("..", models_dir)
            demand_path = os.path.join(alt_models_dir, "demand_model.pkl")
            solar_path = os.path.join(alt_models_dir, "solar_model.pkl")

        if not os.path.exists(demand_path) or not os.path.exists(solar_path):
            raise FileNotFoundError(f"Model artifacts not found in {models_dir}")

        self.demand_artifact = joblib.load(demand_path)
        self.solar_artifact = joblib.load(solar_path)

        self.demand_model = self.demand_artifact["model"]
        self.solar_model = self.solar_artifact["model"]

        self.demand_features = self.demand_artifact["features"]
        self.solar_features = self.solar_artifact["features"]
        self.version = self.demand_artifact.get("version", "v1.0.0")

    def predict_demand(self, features_dict: Dict[str, Any]) -> float:
        """Generates single-step demand prediction (kW)."""
        df = pd.DataFrame([features_dict])
        for col in self.demand_features:
            if col not in df.columns:
                df[col] = 0.0
        X = df[self.demand_features]
        pred = float(self.demand_model.predict(X)[0])
        return max(0.0, round(pred, 2))

    def predict_solar(self, features_dict: Dict[str, Any]) -> float:
        """Generates single-step solar generation prediction (kW)."""
        df = pd.DataFrame([features_dict])
        for col in self.solar_features:
            if col not in df.columns:
                df[col] = 0.0
        X = df[self.solar_features]
        pred = float(self.solar_model.predict(X)[0])
        return max(0.0, round(pred, 2))

if __name__ == "__main__":
    predictor = GreenGridPredictor()
    sample_features = {
        "hour": 14,
        "day_of_week": 2,
        "is_weekend": 0,
        "month": 6,
        "temperature": 32.5,
        "humidity": 55.0,
        "cloud_cover": 15.0,
        "solar_radiation": 750.0,
        "sin_hour": np.sin(2 * np.pi * 14 / 24.0),
        "cos_hour": np.cos(2 * np.pi * 14 / 24.0),
        "sin_month": np.sin(2 * np.pi * 6 / 12.0),
        "cos_month": np.cos(2 * np.pi * 6 / 12.0),
        "lag_1_demand": 28.5,
        "lag_24_demand": 26.0,
        "rolling_3h_demand": 27.8
    }

    dem_pred = predictor.predict_demand(sample_features)
    sol_pred = predictor.predict_solar(sample_features)

    print("--- Inference Sample Prediction ---")
    print(f"Predicted Demand : {dem_pred} kW")
    print(f"Predicted Solar  : {sol_pred} kW")
