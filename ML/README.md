# ML — GreenGrid AI

Pipeline (from synopsis sec. 16):
Historical Data -> Data Cleaning -> Feature Engineering -> Train/Test Split -> ML Model -> Model Evaluation -> Prediction -> Optimization Engine -> Dashboard

## Models
- **Demand prediction**: Random Forest / XGBoost (hackathon), LSTM (advanced)
- **Solar generation prediction**: function of time, solar radiation, temperature, weather, historical generation

## Sample metrics to beat
| Metric | Value |
|---|---|
| MAE | 0.32 kWh |
| RMSE | 0.47 kWh |
| R² | 0.91 |

## TODO
- [ ] Load / simulate dataset (energy_data table columns)
- [ ] Feature engineering: hour, day, weekend flag, previous-hour/day consumption, rolling averages
- [ ] Train demand model, save as `demand_model.pkl`
- [ ] Train solar model, save as `solar_model.pkl`
- [ ] Expose both via `backend/main.py` forecast endpoints
