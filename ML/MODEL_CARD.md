# GreenGrid AI — Machine Learning Model Card

> **Version:** 1.0.0  
> **Target Models:** Demand Prediction (`energy_demand`) & Solar Generation Prediction (`solar_generation`)  
> **Model Architecture:** Random Forest Regressor (`scikit-learn`)  
> **Date:** August 22, 2026

---

## 1. Synthetic Data Warning

>  **SYNTHETIC DATA WARNING:**  
> The models described in this card were trained on a 100% synthetic dataset (`DB/greengrid_ai_synthetic_dataset.csv`, 8,760 hourly rows). All values are generated from parametric formulas with random noise (seed 42). They must be used **only for hackathon demonstration and prototyping purposes** — never for real-world grid operations or financial commitments.

---

## 2. Model 1: Electricity Demand Predictor

### Overview
- **Target Variable:** `energy_demand` (Kilowatts / kW)
- **Model Type:** `sklearn.ensemble.RandomForestRegressor` (`n_estimators=150`, `max_depth=12`, `random_state=42`)
- **Artifact File:** `ML/models/demand_model.pkl`

### Features Used (14)
- Calendar & Cyclical: `hour`, `day_of_week`, `is_weekend`, `month`, `sin_hour`, `cos_hour`, `sin_month`, `cos_month`
- Weather Features: `temperature` (°C), `humidity` (%), `cloud_cover` (%)
- Autoregressive Lag Features: `lag_1_demand` (previous hour load), `lag_24_demand` (same hour yesterday), `rolling_3h_demand` (3-hour moving average)

### Data Split Strategy (Chronological)
- **Train Set:** First 70% of dataset (Jan 1 – Sep 13, 2023, 6,115 rows)
- **Validation Set:** Next 15% of dataset (Sep 14 – Nov 7, 2023, 1,310 rows)
- **Test Set:** Final 15% of dataset (Nov 8 – Dec 31, 2023, 1,311 rows)

### Performance Evaluation Metrics
| Split | MAE (kW) | RMSE (kW) | R² Score |
|---|---|---|---|
| **Train Set** | 0.5880 | 0.7421 | 0.9828 |
| **Validation Set** | 0.9173 | 1.1556 | 0.9310 |
| **Test Set** | 0.9553 | 1.2133 | **0.9236** |

---

## 3. Model 2: Solar Generation Predictor

### Overview
- **Target Variable:** `solar_generation` (Kilowatts / kW)
- **Model Type:** `sklearn.ensemble.RandomForestRegressor` (`n_estimators=150`, `max_depth=12`, `random_state=42`)
- **Artifact File:** `ML/models/solar_model.pkl`

### Features Used (10)
- Calendar & Cyclical: `hour`, `month`, `sin_hour`, `cos_hour`, `sin_month`, `cos_month`
- Solar & Weather Features: `solar_radiation` (W/m²), `cloud_cover` (%), `temperature` (°C), `humidity` (%)

### Data Split Strategy (Chronological)
- **Train Set:** First 70% of dataset (Jan 1 – Sep 13, 2023, 6,115 rows)
- **Validation Set:** Next 15% of dataset (Sep 14 – Nov 7, 2023, 1,310 rows)
- **Test Set:** Final 15% of dataset (Nov 8 – Dec 31, 2023, 1,311 rows)

### Performance Evaluation Metrics
| Split | MAE (kW) | RMSE (kW) | R² Score |
|---|---|---|---|
| **Train Set** | 0.1416 | 0.2786 | 0.9995 |
| **Validation Set** | 0.3386 | 0.6973 | 0.9976 |
| **Test Set** | 0.3363 | 0.7324 | **0.9979** |

---

## 4. Anti-Data-Leakage Safeguards

To ensure valid time-series forecasting:
1. Downstream optimization outputs (`battery_soc`, `battery_power`, `grid_power`) were strictly excluded from feature sets.
2. Chronological data splitting (no random K-Fold cross validation or shuffling) prevented future observation leakage into historical training windows.
3. Lag features (`lag_1_demand`, `lag_24_demand`, `rolling_3h_demand`) were computed chronologically before windowing.

---

## 5. Model Limitations

1. **Synthetic Weather Dynamics:** Weather dynamics are smooth sinusoids with Gaussian noise; unexpected weather events (extreme storms, solar eclipses) are unmodeled.
2. **Single Campus Load Profile:** Scaled specifically for a 50 kW solar array / 100 kWh battery campus load profile.
3. **No External Calendar Events:** Public holidays, campus closures, and exam periods are not explicitly encoded.
