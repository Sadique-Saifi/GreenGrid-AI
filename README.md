# 🌱 GreenGrid AI

**AI-Powered Renewable Energy Demand Prediction & Optimization System**

GreenGrid AI doesn't just predict energy demand — it decides how renewable energy, battery storage, and grid electricity should be coordinated to minimize waste, cost, and carbon emissions.

---

##  📌 Overview

Renewable energy generation (solar) rarely lines up with demand — surplus at noon, shortfall in the evening. GreenGrid AI solves this by:

1. **Predicting** future electricity demand and solar generation using ML
2. **Optimizing** the split between Solar → Load, Solar → Battery, Battery → Load, and Grid → Load
3. **Explaining** every decision through a live dashboard with cost/CO₂ impact

---

##    Key Features

- 🔴 **Live Dashboard** — real-time solar, demand, battery SOC, grid usage, renewable %, and CO₂ avoided
- 📊 **Analytics** — 7/14/30-day historical generation vs. consumption, CSV export
- 🔮 **Forecast** — 6h/12h/24h demand & solar predictions with confidence intervals
- ⚡ **Optimization Engine** — live allocation table + "Why did the AI decide this?" explainability panel
- 🎛️ **What-If Simulator** — drag sliders (solar/demand/battery) or trigger cloudy/peak-demand scenarios
- ⚙️ **Config Panel** — capacity, SOC limits, and system toggles (auto-optimize, alerts, grid export)

---

##    System Architecture

```
Energy & Weather Data → Preprocessing → ML Models (Demand + Solar Prediction)
        → Optimization Engine → Solar/Battery/Grid Allocation → Dashboard
```

**Flow:** Frontend (fetch/HTTP) → FastAPI Backend → ML Inference + Rule-based Optimizer → PostgreSQL ↔ IoT/ESP32 (future)

---

##    Core Modules

| Module | Function |
|---|---|
| Data Collection | Hourly energy/weather data (temp, humidity, solar radiation, demand, SOC) |
| Preprocessing | Cleaning, date/time features, lag & rolling averages |
| Demand Prediction | Random Forest / XGBoost (LSTM planned) |
| Solar Prediction | Forecasts generation from time, radiation, weather |
| Optimization Engine | Compares predicted supply vs. demand, allocates energy |
| Battery Management | Tracks SOC, recommends charge/discharge |
| Smart Recommendations | Converts optimizer output into plain-language guidance |

---

##    Tech Stack

| Layer | Technologies |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JS, Chart.js |
| Backend | Python, FastAPI, Uvicorn |
| Machine Learning | Pandas, NumPy, Scikit-learn, XGBoost |
| Database | PostgreSQL (Neon) |
| IoT (future) | ESP32, current/voltage/solar sensors |
| Deployment | AWS / Render / Railway |

---

## 📁 Project Structure

```
GreenGridAI/
├── frontend/
│   ├── index.html        # Dashboard
│   ├── pages/             # Analytics, Forecast, Optimization, Simulator, Config
│   ├── css/
│   └── js/
├── backend/
│   └── main.py            # FastAPI app
├── ML/
│   └── train.py           # Training pipeline
└── DB/
    └── schema.sql          # PostgreSQL schema
```

---

##    Database Schema

| Table | Key Fields |
|---|---|
| `energy_data` | timestamp, energy_consumption, solar_generation, temperature, humidity, solar_radiation, weather |
| `battery_data` | timestamp, battery_soc, charging_rate, discharging_rate |
| `predictions` | timestamp, predicted_demand, predicted_generation |
| `optimization_results` | timestamp, solar_usage, battery_usage, grid_usage, energy_saved, cost_saved, co2_reduced |

---

##    API Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /energy/current` | Live snapshot (solar, demand, battery, grid) |
| `GET /energy/history` | Historical data for charts |
| `GET /forecast/demand` | Predicted demand + peak window |
| `GET /forecast/solar` | Predicted solar generation |
| `GET /battery/status` | Battery SOC & charge/discharge rate |
| `GET /optimization/recommendation` | Allocation breakdown + reasoning |
| `GET /dashboard/summary` | Aggregated dashboard metrics |
| `POST /energy/data` | Ingest sensor/simulated readings |

---

##    Getting Started

**Frontend** (no build step):
```bash
open frontend/index.html
```

**Backend:**
```bash
cd backend
pip install fastapi uvicorn
uvicorn main:app --reload
```

---

##    Sample Model Metrics

| Metric | Value |
|---|---|
| MAE | 0.32 kWh |
| RMSE | 0.47 kWh |
| R² | 0.91 |

##    Sample Sustainability Impact

| Metric | Value |
|---|---|
| Renewable Energy Used | 82% |
| Grid Energy Reduced | 31% |
| Cost Saved | ₹1,250 / day |
| CO₂ Avoided | 18.4 kg / day |

---

##    Target Users
Residential buildings · Schools/Colleges · Offices · Hospitals · Hotels · Small Industries · Microgrids

##    Future Scope
- Real IoT integration (smart meters, ESP32)
- Live weather API + LSTM forecasting
- Dynamic electricity pricing
- Reinforcement learning-based optimization
- Multi-building microgrid support

---

##    Team

| Role | Focus |
|---|---|
| ML/Data | Dataset, preprocessing, prediction models |
| Backend | FastAPI, database, ML integration |
| Frontend | Dashboard, charts, UI/UX |
| Optimization & Presentation | Optimization logic, battery sim, pitch |

---

##  📄 License
MIT License — free to use and modify.

---
  
