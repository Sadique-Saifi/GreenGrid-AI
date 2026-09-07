"""
GreenGrid AI — Data Preprocessing & Feature Engineering Module
Handles dataset loading, feature creation (cyclical encodings, lags, rolling windows),
and chronological train/validation/test splitting.
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any

# Feature definitions to prevent data leakage
DEMAND_FEATURES = [
    "hour", "day_of_week", "is_weekend", "month",
    "temperature", "humidity", "cloud_cover",
    "sin_hour", "cos_hour", "sin_month", "cos_month",
    "lag_1_demand", "lag_24_demand", "rolling_3h_demand"
]

SOLAR_FEATURES = [
    "hour", "month", "solar_radiation", "cloud_cover",
    "temperature", "humidity",
    "sin_hour", "cos_hour", "sin_month", "cos_month"
]

def load_raw_dataset(csv_path: str = "DB/greengrid_ai_synthetic_dataset.csv") -> pd.DataFrame:
    """Loads the raw CSV dataset and parses timestamp."""
    if not os.path.exists(csv_path):
        # Fallback if executed inside ml/ directory
        alt_path = os.path.join("..", csv_path)
        if os.path.exists(alt_path):
            csv_path = alt_path
        else:
            raise FileNotFoundError(f"Dataset file not found at {csv_path}")

    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineers cyclical time features and lag features while avoiding target data leakage.
    """
    df = df.copy()

    # Cyclical encodings for hour (24-hour cycle) and month (12-month cycle)
    df["sin_hour"] = np.sin(2 * np.pi * df["hour"] / 24.0)
    df["cos_hour"] = np.cos(2 * np.pi * df["hour"] / 24.0)
    df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12.0)
    df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12.0)

    # Lag features for energy demand
    df["lag_1_demand"] = df["energy_demand"].shift(1)
    df["lag_24_demand"] = df["energy_demand"].shift(24)
    df["rolling_3h_demand"] = df["energy_demand"].shift(1).rolling(window=3).mean()

    # Drop rows with NaN caused by shifting
    df = df.dropna().reset_index(drop=True)
    return df

def get_chronological_splits(df: pd.DataFrame, train_ratio: float = 0.70, val_ratio: float = 0.15) -> Dict[str, pd.DataFrame]:
    """
    Splits time-series dataset chronologically without random shuffling to prevent data leakage.
    - Train: First 70% (~6,100 hours)
    - Validation: Next 15% (~1,300 hours)
    - Test: Final 15% (~1,300 hours)
    """
    n = len(df)
    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train_df = df.iloc[:train_end].copy()
    val_df = df.iloc[train_end:val_end].copy()
    test_df = df.iloc[val_end:].copy()

    return {
        "train": train_df,
        "val": val_df,
        "test": test_df
    }

def prepare_demand_datasets(csv_path: str = "DB/greengrid_ai_synthetic_dataset.csv"):
    """Returns X, y dataframes for demand model training and evaluation."""
    raw_df = load_raw_dataset(csv_path)
    df = engineer_features(raw_df)
    splits = get_chronological_splits(df)

    return (
        splits["train"][DEMAND_FEATURES], splits["train"]["energy_demand"],
        splits["val"][DEMAND_FEATURES], splits["val"]["energy_demand"],
        splits["test"][DEMAND_FEATURES], splits["test"]["energy_demand"]
    )

def prepare_solar_datasets(csv_path: str = "DB/greengrid_ai_synthetic_dataset.csv"):
    """Returns X, y dataframes for solar model training and evaluation."""
    raw_df = load_raw_dataset(csv_path)
    df = engineer_features(raw_df)
    splits = get_chronological_splits(df)

    return (
        splits["train"][SOLAR_FEATURES], splits["train"]["solar_generation"],
        splits["val"][SOLAR_FEATURES], splits["val"]["solar_generation"],
        splits["test"][SOLAR_FEATURES], splits["test"]["solar_generation"]
    )
