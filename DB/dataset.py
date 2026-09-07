"""
GreenGrid AI - SYNTHETIC Hourly Energy Dataset Generator
==========================================================
Generates 8,760 hourly records (365 days x 24 hours, non-leap year 2023)
with physically-plausible, CORRELATED relationships between weather,
solar generation, electricity demand, battery state, and grid usage.

*** THIS DATA IS 100% SYNTHETIC / SIMULATED ***
It is generated from parametric formulas + noise. It does NOT represent
any real building, meter, sensor, or utility. It is intended ONLY for
prototyping and testing the GreenGrid AI ML/optimization pipeline
(e.g. for a hackathon demo), and must never be presented as real-world
consumption or generation data.

Reproducibility: fixed random seed (SEED = 42).
Climate assumption: subtropical, Northern-India-like site (~28°N, similar
to Delhi) — chosen because the source project synopsis quotes costs in
Rupees. Change LATITUDE_PROFILE constants below to model a different site.
"""

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# 0. CONFIG / REPRODUCIBILITY
# ----------------------------------------------------------------------
SEED = 42
rng = np.random.default_rng(SEED)

YEAR = 2023  # non-leap year -> 365 days -> 8,760 hourly records
N_HOURS = 24 * 365
assert N_HOURS == 8760

# Site / system assumptions (kept consistent with the project synopsis:
# 50 kW solar array, 100 kWh battery, campus-scale demand)
SOLAR_CAPACITY_KW = 50.0
BATTERY_CAPACITY_KWH = 100.0
BATTERY_MIN_SOC = 10.0          # % - avoid deep discharge
BATTERY_MAX_SOC = 100.0
BATTERY_MAX_CHARGE_KW = 20.0
BATTERY_MAX_DISCHARGE_KW = 20.0
BATTERY_ROUND_TRIP_EFF = 0.92   # charging/discharging losses
INITIAL_SOC = 50.0

# ----------------------------------------------------------------------
# 1. TIME INDEX
# ----------------------------------------------------------------------
timestamps = pd.date_range(start=f"{YEAR}-01-01 00:00:00", periods=N_HOURS, freq="h")

df = pd.DataFrame({"timestamp": timestamps})
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek       # 0=Mon ... 6=Sun
df["month"] = df["timestamp"].dt.month
df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)
day_of_year = df["timestamp"].dt.dayofyear.values

# ----------------------------------------------------------------------
# 2. WEATHER: temperature, humidity, solar radiation, cloud cover
#    (all correlated with season + time of day, plus noise)
# ----------------------------------------------------------------------
hour = df["hour"].values.astype(float)

# --- Seasonal temperature curve ---------------------------------------
# Peak around day ~170 (mid-June), trough around day ~15 (mid-Jan),
# mimicking a hot subtropical climate (hot summer, mild winter, monsoon).
seasonal_temp = 24 + 14 * np.cos(2 * np.pi * (day_of_year - 170) / 365)
# --- Diurnal temperature swing: coolest ~05:00, warmest ~15:00 --------
diurnal_temp = 6.5 * np.sin(2 * np.pi * (hour - 9) / 24)
temperature = seasonal_temp + diurnal_temp + rng.normal(0, 1.3, N_HOURS)
temperature = np.clip(temperature, -2, 48)

# --- Monsoon flag (Jul-Sep): raises humidity & cloud cover, cools temp a touch
month_arr = df["month"].values
is_monsoon = np.isin(month_arr, [7, 8, 9]).astype(float)
temperature = temperature - is_monsoon * 2.0 + rng.normal(0, 0.5, N_HOURS)

# --- Cloud cover (%): baseline low in winter/summer, high in monsoon --
cloud_base = 20 + 45 * is_monsoon + 10 * np.isin(month_arr, [1, 2, 12]).astype(float)
cloud_noise = rng.normal(0, 12, N_HOURS)
# short autocorrelated "weather system" component so cloud cover isn't iid
cloud_ar = np.zeros(N_HOURS)
prev = 0.0
for i in range(N_HOURS):
    prev = 0.85 * prev + rng.normal(0, 8)
    cloud_ar[i] = prev
cloud_cover = np.clip(cloud_base + cloud_noise + cloud_ar, 0, 100)

# --- Humidity (%): inversely related to temperature, up in monsoon ----
humidity = 55 - 0.55 * (temperature - 24) + 25 * is_monsoon + rng.normal(0, 5, N_HOURS)
humidity = humidity + 0.15 * cloud_cover  # cloudier -> more humid
humidity = np.clip(humidity, 10, 98)

# --- Solar radiation (W/m^2): daylight bell curve modulated by season
#     (day length) and reduced by cloud cover -------------------------
# Day-length factor: shorter days in winter, longer in summer.
day_length_factor = 1 + 0.18 * np.cos(2 * np.pi * (day_of_year - 172) / 365 + np.pi)
sunrise = 6.0 - 0.9 * np.cos(2 * np.pi * (day_of_year - 172) / 365)   # ~5.1 to ~6.9
sunset = 18.0 + 0.9 * np.cos(2 * np.pi * (day_of_year - 172) / 365)   # ~17.1 to ~18.9

daylight_mask = (hour >= sunrise) & (hour <= sunset)
solar_angle = np.where(
    daylight_mask,
    np.sin(np.pi * (hour - sunrise) / np.clip(sunset - sunrise, 1e-6, None)),
    0.0,
)
solar_angle = np.clip(solar_angle, 0, None)

clear_sky_radiation = 950 * day_length_factor * solar_angle
cloud_attenuation = 1 - 0.78 * (cloud_cover / 100.0)   # clouds cut radiation
solar_radiation = clear_sky_radiation * cloud_attenuation
solar_radiation += rng.normal(0, 12, N_HOURS)
solar_radiation = np.clip(solar_radiation, 0, 1100)
solar_radiation[~daylight_mask] = np.clip(
    solar_radiation[~daylight_mask] * 0 + rng.normal(0, 1.5, (~daylight_mask).sum()), 0, None
)  # ~zero at night with tiny sensor noise floor

df["temperature"] = np.round(temperature, 2)
df["humidity"] = np.round(humidity, 2)
df["solar_radiation"] = np.round(solar_radiation, 2)
df["cloud_cover"] = np.round(cloud_cover, 2)

# ----------------------------------------------------------------------
# 3. SOLAR GENERATION (kW) - driven by radiation, with panel efficiency,
#    temperature derating, and inverter/system losses + noise
# ----------------------------------------------------------------------
PANEL_REF_EFFICIENCY = SOLAR_CAPACITY_KW / 1000.0  # kW per (W/m^2) at STC=1000W/m^2
temp_derate = 1 - 0.004 * np.clip(df["temperature"].values - 25, 0, None)  # hot panels lose eff.
inverter_eff = 0.96

solar_generation = (
    df["solar_radiation"].values * PANEL_REF_EFFICIENCY * temp_derate * inverter_eff
)
solar_generation *= rng.normal(1.0, 0.035, N_HOURS)  # small stochastic system noise
solar_generation = np.clip(solar_generation, 0, SOLAR_CAPACITY_KW)
solar_generation[~daylight_mask] = np.clip(
    rng.normal(0, 0.02, (~daylight_mask).sum()), 0, None
)  # ~0 at night
df["solar_generation"] = np.round(solar_generation, 3)

# ----------------------------------------------------------------------
# 4. ELECTRICITY DEMAND (kW) - base load + morning/evening peaks +
#    weekday/weekend pattern + temperature-driven cooling load + noise
# ----------------------------------------------------------------------
is_weekend = df["is_weekend"].values.astype(bool)

# Weekday profile: base load with morning (7-9) and evening (18-21) peaks
weekday_shape = (
    1.0
    + 0.55 * np.exp(-0.5 * ((hour - 8) / 1.6) ** 2)     # morning peak
    + 0.85 * np.exp(-0.5 * ((hour - 19.5) / 2.0) ** 2)  # evening peak
    - 0.30 * np.exp(-0.5 * ((hour - 3) / 2.5) ** 2)     # overnight dip
)
# Weekend profile: flatter, later/broader midday peak, lower evening peak
weekend_shape = (
    1.0
    + 0.35 * np.exp(-0.5 * ((hour - 11) / 3.0) ** 2)    # late-morning/midday
    + 0.40 * np.exp(-0.5 * ((hour - 20) / 2.5) ** 2)    # smaller evening peak
    - 0.25 * np.exp(-0.5 * ((hour - 3.5) / 2.5) ** 2)
)
demand_shape = np.where(is_weekend, weekend_shape, weekday_shape)

BASE_LOAD_KW = 14.0  # campus-scale baseline
seasonal_demand_mult = 1 + 0.02 * (df["month"].isin([6, 7, 8]).astype(float))  # slight seasonal bump

# Cooling load: demand rises when it's hot (AC usage), esp. above ~28C
cooling_load = 0.55 * np.clip(df["temperature"].values - 28, 0, None)

energy_demand = (
    BASE_LOAD_KW * demand_shape * seasonal_demand_mult.values
    + cooling_load
    + rng.normal(0, 1.1, N_HOURS)
)
energy_demand = np.clip(energy_demand, 2.0, None)  # never fully zero (always some baseline load)
df["energy_demand"] = np.round(energy_demand, 3)

# ----------------------------------------------------------------------
# 5. BATTERY + GRID SIMULATION (sequential - depends on previous hour's SOC)
#    Simplified rule-based optimizer mirroring the synopsis's logic:
#      - If solar > demand: serve load from solar, charge battery with surplus
#      - If solar < demand: serve shortfall from battery, then grid
#      - Battery power convention: + = charging, - = discharging
#      - Grid power convention: >= 0 (import only); excess surplus beyond
#        a full battery is curtailed (not exported) - see limitations.
# ----------------------------------------------------------------------
soc = np.zeros(N_HOURS)
battery_power = np.zeros(N_HOURS)
grid_power = np.zeros(N_HOURS)

current_soc = INITIAL_SOC  # %
solar_arr = df["solar_generation"].values
demand_arr = df["energy_demand"].values

for i in range(N_HOURS):
    solar_kw = solar_arr[i]
    demand_kw = demand_arr[i]
    net = solar_kw - demand_kw  # positive = surplus, negative = deficit

    soc_kwh = current_soc / 100.0 * BATTERY_CAPACITY_KWH
    headroom_kwh = (BATTERY_MAX_SOC - current_soc) / 100.0 * BATTERY_CAPACITY_KWH
    available_kwh = (current_soc - BATTERY_MIN_SOC) / 100.0 * BATTERY_CAPACITY_KWH
    available_kwh = max(available_kwh, 0.0)

    if net >= 0:
        # Surplus solar: charge battery first (up to max charge rate & headroom)
        charge_kw = min(net, BATTERY_MAX_CHARGE_KW, headroom_kwh / (1 * BATTERY_ROUND_TRIP_EFF))
        charge_kw = max(charge_kw, 0.0)
        soc_kwh_new = soc_kwh + charge_kw * BATTERY_ROUND_TRIP_EFF * 1.0  # 1-hour step
        battery_power[i] = charge_kw            # + = charging
        remaining_surplus = net - charge_kw
        grid_power[i] = 0.0                     # curtail any leftover surplus (no export modeled)
    else:
        deficit = -net
        discharge_kw = min(deficit, BATTERY_MAX_DISCHARGE_KW, available_kwh / 1.0)
        discharge_kw = max(discharge_kw, 0.0)
        soc_kwh_new = soc_kwh - discharge_kw
        battery_power[i] = -discharge_kw        # - = discharging
        remaining_deficit = deficit - discharge_kw
        grid_power[i] = max(remaining_deficit, 0.0)

    soc_kwh_new = np.clip(soc_kwh_new, BATTERY_MIN_SOC / 100.0 * BATTERY_CAPACITY_KWH,
                           BATTERY_MAX_SOC / 100.0 * BATTERY_CAPACITY_KWH)
    current_soc = soc_kwh_new / BATTERY_CAPACITY_KWH * 100.0
    # small measurement noise on SOC reading (sensor noise), still clipped to valid range
    soc[i] = np.clip(current_soc + rng.normal(0, 0.15), 0, 100)

df["battery_soc"] = np.round(soc, 2)
df["battery_power"] = np.round(battery_power, 3)
df["grid_power"] = np.round(np.clip(grid_power, 0, None), 3)

# ----------------------------------------------------------------------
# 6. FINAL COLUMN ORDER, LABELLING, SANITY CLIPS
# ----------------------------------------------------------------------
COLUMNS = [
    "timestamp", "hour", "day_of_week", "month", "is_weekend",
    "temperature", "humidity", "solar_radiation", "cloud_cover",
    "energy_demand", "solar_generation", "battery_soc", "battery_power", "grid_power",
]
df = df[COLUMNS]
df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%dT%H:%M:%S")

assert df["timestamp"].nunique() == 8760, "Duplicate timestamps found!"
assert df.shape[0] == 8760
assert (df["battery_soc"].between(0, 100)).all()
assert (df["solar_generation"] >= 0).all()
assert (df["energy_demand"] > 0).all()
assert (df["grid_power"] >= 0).all()
assert (df["humidity"].between(0, 100)).all()
assert (df["cloud_cover"].between(0, 100)).all()

OUT_PATH = "greengrid_ai_synthetic_dataset.csv"
df.to_csv(OUT_PATH, index=False)
print(f"Saved {len(df)} rows to {OUT_PATH}")
print(df.head(10).to_string(index=False))