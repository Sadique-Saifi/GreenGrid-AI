# GreenGrid AI — Data Quality & Exploratory Analysis Report

> **Dataset:** `DB/greengrid_ai_synthetic_dataset.csv`  
> **Date:** August 22, 2026  
> **Status:** Inspected & Verified for ML Pipeline Training

---

## 1. Executive Summary

A comprehensive exploratory analysis was performed on the `greengrid_ai_synthetic_dataset.csv` dataset. The dataset consists of exactly **8,760 hourly rows** representing a full 365-day calendar year (Jan 1, 2023 – Dec 31, 2023). 

No missing values, duplicate timestamps, or unphysical outliers were identified. Data leakage risks were explicitly analyzed: downstream simulation outputs (`battery_soc`, `battery_power`, `grid_power`) have been flagged and isolated from predictor feature sets. Both primary targets (`energy_demand` and `solar_generation`) are present, continuous, and suitable for supervised machine learning regression.

---

## 2. Detailed 20-Point Inspection Findings

| # | Inspection Check | Result | Details / Metrics |
|---|---|---|---|
| 1 | **Number of Rows** | `8,760` | Exactly 365 days × 24 hours. |
| 2 | **Number of Columns** | `14` | `timestamp`, `hour`, `day_of_week`, `month`, `is_weekend`, `temperature`, `humidity`, `cloud_cover`, `solar_radiation`, `energy_demand`, `solar_generation`, `battery_soc`, `battery_power`, `grid_power`. |
| 3 | **Data Types** | Validated | `timestamp` (ISO datetime string), `hour`/`day_of_week`/`month`/`is_weekend` (Integer), remaining 9 features (Float64). |
| 4 | **Missing Values** | `0` | Zero null or NaN entries across all 14 columns. |
| 5 | **Duplicate Timestamps** | `0` | Every hourly timestamp is unique. |
| 6 | **Duplicate Rows** | `0` | Zero duplicate rows found. |
| 7 | **Negative Values** | Validated | `temperature` min is -2.0°C (valid winter low); `battery_power` min is -20.0 kW (valid discharging sign convention); all generation/demand/radiation values ≥ 0. |
| 8 | **Outliers** | None | Max solar generation = 50.0 kW (matches panel rating); max demand = 36.19 kW; max radiation = 1100.0 W/m². All values fall within physical bounds. |
| 9 | **Timestamp Continuity** | Continuous | Hourly frequency (`freq='h'`) uninterrupted from `2023-01-01 00:00:00` to `2023-12-31 23:00:00`. |
| 10 | **Min / Max Range** | Validated | `energy_demand`: [2.1, 36.19] kW; `solar_generation`: [0.0, 50.0] kW; `temperature`: [-2.0, 47.78] °C; `humidity`: [10.0, 98.0] %. |
| 11 | **Mean & Std Dev** | Validated | `energy_demand`: Mean = 17.97 kW, Std = 5.44 kW; `solar_generation`: Mean = 10.22 kW, Std = 13.44 kW; `temperature`: Mean = 23.50 °C, Std = 10.67 °C. |
| 12 | **Feature Correlations** | Analyzed | `energy_demand` correlates with `hour` (r = +0.669) and `temperature` (r = +0.552). `solar_generation` correlates with `solar_radiation` (r = +0.9986) and `cloud_cover` (r = -0.354). |
| 13 | **Nighttime Solar Generation** | Verified `≈ 0` | Mean nighttime generation (hours < 5 or > 21) = 0.0076 kW (max 0.12 kW, practically zero). |
| 14 | **Cloud Cover Effect** | Confirmed | Negative correlation with solar generation (r = -0.354). High cloud cover significantly reduces generation. |
| 15 | **Solar Radiation Effect** | Confirmed | Near-perfect positive correlation (r = +0.9986). Solar generation is direct linear function of solar irradiance. |
| 16 | **Demand Variation by Hour** | Confirmed | Strong diurnal curve (r = +0.669), with morning (7–9 AM) and evening (6:30–9:30 PM) peaks. |
| 17 | **Demand Variation by Day** | Confirmed | Weekdays show higher average demand (18.2 kW) compared to weekends (17.5 kW). |
| 18 | **Seasonal Patterns** | Confirmed | Summer months (May–June) exhibit peak demand due to AC cooling loads (temperature up to 47.8°C); monsoon (Jul–Sep) shows reduced solar generation. |
| 19 | **Data Leakage Risk** | Flagged & Isolated | `battery_soc`, `battery_power`, and `grid_power` are **downstream outputs** of optimization logic. Excluded from forecasting features to prevent target leakage. |
| 20 | **ML Target Columns** | Present | Both target columns (`energy_demand` and `solar_generation`) exist, are non-null, and ready for model training. |

---

## 3. Statistical Summary Table

| Column | Min | Mean | Std | 50% (Median) | Max |
|---|---|---|---|---|---|
| `hour` | 0.0 | 11.50 | 6.92 | 11.50 | 23.0 |
| `day_of_week` | 0.0 | 2.99 | 2.00 | 3.00 | 6.0 |
| `month` | 1.0 | 6.53 | 3.45 | 7.00 | 12.0 |
| `is_weekend` | 0.0 | 0.28 | 0.45 | 0.00 | 1.0 |
| `temperature` (°C) | -2.00 | 23.50 | 10.67 | 23.31 | 47.78 |
| `humidity` (%) | 10.00 | 66.70 | 14.28 | 64.34 | 98.00 |
| `cloud_cover` (%) | 0.00 | 35.22 | 25.38 | 32.00 | 100.00 |
| `solar_radiation` (W/m²) | 0.00 | 216.71 | 284.15 | 4.08 | 1100.00 |
| `energy_demand` (kW) | 2.10 | 17.97 | 5.44 | 17.86 | 36.19 |
| `solar_generation` (kW) | 0.00 | 10.22 | 13.44 | 0.06 | 50.00 |
| `battery_soc` (%) | 0.00 | 25.18 | 26.70 | 10.12 | 100.00 |
| `battery_power` (kW) | -20.00 | 0.19 | 8.78 | 0.00 | 20.00 |
| `grid_power` (kW) | 0.00 | 8.69 | 8.11 | 9.40 | 36.19 |

---

## 4. Modeling Strategy & Feature Selection

To prevent data leakage in time-series forecasting:
1. **Demand Model (`energy_demand`)**:
   - Features: `hour`, `day_of_week`, `is_weekend`, `month`, `temperature`, `humidity`, `cloud_cover`, `sin_hour`, `cos_hour`, `sin_month`, `cos_month`, `lag_1_demand`, `lag_24_demand`, `rolling_3h_demand`.
2. **Solar Model (`solar_generation`)**:
   - Features: `hour`, `month`, `solar_radiation`, `cloud_cover`, `temperature`, `sin_hour`, `cos_hour`, `sin_month`, `cos_month`.
3. **Split Strategy**: Chronological split (70% Train, 15% Validation, 15% Test) to ensure strict temporal evaluation.
