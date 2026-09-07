# GreenGrid AI — Synthetic Dataset Documentation

> ⚠️ **THIS DATASET IS 100% SYNTHETIC.** Every value is generated from parametric
> formulas plus random noise (fixed seed = 42). It does **not** represent any real
> building, meter, sensor, utility, or weather station. It must be used only for
> prototyping / demoing the GreenGrid AI ML and optimization pipeline — never
> presented as real electricity consumption or solar production data.

Files delivered:
- `generate_dataset.py` — reproducible Python (pandas + numpy) generation script
- `greengrid_ai_synthetic_dataset.csv` — 8,760 hourly rows (Jan 1 – Dec 31, 2023)
- this documentation file

---

## 1. Assumptions

| Assumption | Value / Choice | Why |
|---|---|---|
| Year | 2023 (non-leap) | Gives exactly 365 × 24 = 8,760 rows |
| Climate | Subtropical, ~28°N (Delhi-like) | Source synopsis quotes costs in ₹ (Rupees) |
| Seasons modeled | Winter (mild), pre-monsoon summer (hot, up to ~45°C), monsoon (Jul–Sep, cloudy/humid), post-monsoon/autumn | Matches North-Indian annual weather cycle |
| Solar array | 50 kW capacity | Matches the campus example in the project synopsis |
| Battery | 100 kWh capacity, 10–100% usable SOC band, ±20 kW max charge/discharge, 92% round-trip efficiency | Matches synopsis's battery example; efficiency loss is a standard li-ion assumption |
| Building type | Campus / institutional load | Matches synopsis's illustrative example |
| Baseline demand | ~14 kW base load, rising to ~20–36 kW at peak | Scaled to be plausible against a 50 kW solar / 100 kWh battery system |
| Grid export | **Not modeled.** Any solar surplus beyond a full battery is curtailed, not exported | Keeps `grid_power` non-negative (import-only), a common simplification for a first prototype — see Limitations |
| Battery control | Simple rule-based optimizer (solar → load → battery → grid), same logic as the synopsis's Section 6 | Matches the project's own MVP optimization logic, not a novel algorithm |

## 2. How Each Variable Was Generated (and how it relates to the targets)

- **timestamp / hour / day_of_week / month / is_weekend** — calendar features derived directly from the hourly time index. These drive nearly everything else (time-of-day and seasonal patterns).
- **temperature** — seasonal sinusoid (peak mid-June, trough mid-January) + a daily sinusoid (cool ~5am, warm ~3pm) + Gaussian noise, with a small monsoon-season cooling adjustment. **Drives** `energy_demand` (cooling/AC load above ~28°C) and `solar_generation` (hot-panel efficiency derating).
- **humidity** — inversely related to temperature, boosted in monsoon months and slightly by cloud cover, plus noise. Included as a realistic weather feature; has a weak negative relationship with demand and solar generation in this simulation.
- **cloud_cover** — seasonal baseline (much higher Jul–Sep) plus an autoregressive "weather system" component (so cloudy/clear spells persist for a few hours rather than flipping randomly) plus noise. **Drives** `solar_radiation` (attenuates clear-sky radiation) and indirectly `solar_generation`.
- **solar_radiation** — a clear-sky bell curve between sunrise and sunset (day length itself varies by season), attenuated by `cloud_cover`, plus sensor noise; forced to ~0 outside daylight hours. **Directly drives** `solar_generation` (correlation ≈ 0.999 in the generated data, as expected since generation is a near-linear function of radiation).
- **energy_demand** — a base load shaped by a weekday profile (morning 7–9am and evening 6:30–9:30pm peaks, overnight dip) or a flatter weekend profile, plus a temperature-driven cooling-load term, plus noise. This is a **target variable**.
- **solar_generation** — `solar_radiation × panel efficiency × temperature-derating × inverter efficiency`, plus small stochastic noise, clipped to `[0, 50 kW]` and forced to ~0 at night. This is a **target variable**.
- **battery_soc / battery_power / grid_power** — produced by a sequential (hour-by-hour) rule-based simulation: solar surplus charges the battery (up to its rate/headroom limits); any remaining deficit after solar+battery draws from the grid. `battery_power` is signed (+charging / −discharging); `grid_power` is import-only (≥ 0); `battery_soc` carries over from the previous hour, so it is inherently autocorrelated and NOT independent noise.

## 3. Basic Statistical Summary

| Column | Mean | Std | Min | Median | Max |
|---|---|---|---|---|---|
| temperature (°C) | 23.5 | 10.7 | -2.0 | 23.3 | 47.8 |
| humidity (%) | 66.7 | 14.3 | 10.0 | 64.3 | 98.0 |
| solar_radiation (W/m²) | 216.7 | 284.1 | 0.0 | 4.1* | 1100.0 |
| cloud_cover (%) | 35.2 | 25.4 | 0.0 | 32.0 | 100.0 |
| energy_demand (kW) | 18.0 | 5.4 | ~2–8 | 17.9 | 36.2 |
| solar_generation (kW) | 10.2 | 13.4 | 0.0 | 0.06* | 50.0 |
| battery_soc (%) | 25.2 | 26.7 | 0.0 | 10.1 | 100.0 |
| battery_power (kW) | 0.19 | 8.8 | -20.0 | 0.0 | 20.0 |
| grid_power (kW) | 8.7 | 8.1 | 0.0 | 9.4 | 36.2 |

*Median for `solar_radiation`/`solar_generation` is low because ~half of all hours are nighttime (value ≈ 0).

**Key sanity correlations observed in the generated data:**
- `solar_generation` ↔ `solar_radiation`: **r ≈ 0.999** (as designed)
- `energy_demand` ↔ `hour`: **r ≈ 0.67** (strong daily pattern)
- `energy_demand` ↔ `temperature`: **r ≈ 0.55** (cooling load effect)
- Mean `solar_generation` during night hours (hour < 5 or > 21): **≈ 0.008 kW** (essentially zero, as required)
- Monthly averages show the monsoon dip in `solar_radiation` (Jul–Sep ≈ 140–150 W/m² vs. ≈ 220–260 W/m² the rest of the year) and a summer peak in `energy_demand` (June ≈ 22.2 kW vs. December ≈ 16.4 kW)
- Weekday average demand (18.2 kW) is higher than weekend average (17.5 kW), as designed

## 4. Data Quality Checks (all passed)

| Check | Result |
|---|---|
| Exactly 8,760 rows | ✅ PASS |
| No duplicate timestamps | ✅ PASS |
| No missing values | ✅ PASS |
| `battery_soc` within [0, 100] | ✅ PASS |
| `solar_generation` within [0, 50] (panel capacity) | ✅ PASS |
| `energy_demand` > 0 for all hours | ✅ PASS |
| `grid_power` ≥ 0 (no impossible negative import) | ✅ PASS |
| `humidity` within [0, 100] | ✅ PASS |
| `cloud_cover` within [0, 100] | ✅ PASS |
| `solar_radiation` ≥ 0 | ✅ PASS |
| Nighttime solar generation ≈ 0 (mean < 0.1 kW) | ✅ PASS |
| `battery_power` within [-20, 20] kW (rated charge/discharge limits) | ✅ PASS |

## 5. Suggested ML Features

For **predicting `energy_demand`**:
`hour`, `day_of_week`, `is_weekend`, `month`, `temperature`, `humidity`, plus engineered features such as: previous-hour demand (lag-1), previous-day same-hour demand (lag-24), a rolling 3-hour/24-hour average of demand, and cyclical encodings of `hour` and `month` (sin/cos transforms) to avoid the false "23 is far from 0" discontinuity.

For **predicting `solar_generation`**:
`hour`, `month`, `solar_radiation`, `cloud_cover`, `temperature`, plus a clear-sky-index style feature (radiation relative to a theoretical clear-sky curve for that hour/day) if you want the model to lean less on the near-perfect radiation→generation relationship and more on weather.

**Avoid as direct inputs to the demand or solar models:** `battery_soc`, `battery_power`, `grid_power` — these are *outputs* of the optimization simulation that itself depends on `energy_demand` and `solar_generation`. Using them as predictors would leak the target through the simulation logic (see Limitations §7).

## 6. Suggested Target Variables

- **Target 1 — `energy_demand`** (kW): regression, e.g. Random Forest / XGBoost baseline, LSTM for a time-series upgrade.
- **Target 2 — `solar_generation`** (kW): regression; note this will score very highly (near R²=1) if `solar_radiation` is included as a feature, since generation is derived almost directly from it — for a more meaningful hackathon demo of "ML forecasting," consider predicting **next-hour** or **next-3-hour** solar generation from *past* radiation/cloud data rather than the same-hour radiation reading.

## 7. Train / Test Split Recommendation

Because this is hourly time-series data, use a **chronological split**, not a random shuffle:
- **Train:** Jan 1 – Oct 31, 2023 (~10 months, ~7,300 rows)
- **Validation:** November 2023 (~720 rows)
- **Test:** December 2023 (~744 rows)

This avoids leaking future information into training (a random 80/20 shuffle would let the model "see" hours adjacent to test hours, inflating accuracy). For quick hackathon iteration, a simpler 80/20 chronological split (first 80% of hours = train, last 20% = test) also works. If you engineer lag features (lag-1, lag-24, rolling averages), make sure the lag windows are computed only from information available at or before the prediction time, and drop the first 24 rows (which lack a full lag-24 history).

## 8. Limitations of This Synthetic Dataset

1. **Single site, single year** — no year-to-year variability, no extreme weather events (heatwaves, storms, grid outages), no equipment degradation over time.
2. **No real export/curtailment market modeling** — solar surplus beyond a full battery is discarded ("curtailed") rather than exported to the grid; a production system with net-metering would need a signed `grid_power` (import/export) instead.
3. **Simplified battery model** — constant round-trip efficiency and charge/discharge limits; no temperature effects on battery performance, no degradation/aging, no minimum-cycle constraints.
4. **Rule-based, not learned, optimizer** — `battery_power`/`grid_power` come from the same simple heuristic described in the project synopsis, not from a trained or optimal controller, so they represent "one reasonable policy," not ground truth.
5. **Circular dependency risk** — `battery_soc`, `battery_power`, and `grid_power` are all *downstream* of `energy_demand` and `solar_generation` within the same hour. They are useful for demoing the *optimization engine*, but should not be fed back in as predictors for the *forecasting* models (data leakage).
6. **Simplified climate model** — temperature/humidity/cloud-cover/radiation are generated from smooth seasonal + diurnal curves with noise, not from an actual meteorological model or historical weather station; unusual local microclimate effects are not captured.
7. **No demand-response, occupancy, or holiday calendar** — public holidays, campus closures, exam periods, etc. are not modeled; only a generic weekday/weekend split is used.
8. **No sensor failure / data-gap simulation** — real IoT deployments would have missing readings, drift, and outliers beyond simple Gaussian noise; this dataset has none, so it will look "cleaner" than a real deployment.
9. **Fixed random seed** — reproducible for grading/demo purposes, but means there is exactly one realization of "weather" and "demand" for the year; don't expect this exact CSV to generalize to other synthetic runs without re-seeding.

**Reminder: do not present any statistic from this file as real-world electricity consumption, solar production, or savings — it is a synthetic prototype dataset only.**
