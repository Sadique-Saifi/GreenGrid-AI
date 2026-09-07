-- ============================================================
-- GreenGrid AI — Database schema (from Project Synopsis, sec. 14)
-- ============================================================

CREATE TABLE energy_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    energy_consumption FLOAT,
    solar_generation FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    solar_radiation FLOAT,
    weather VARCHAR(50)
);

CREATE TABLE battery_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    battery_soc FLOAT,
    charging_rate FLOAT,
    discharging_rate FLOAT
);

CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    predicted_demand FLOAT,
    predicted_generation FLOAT
);

CREATE TABLE optimization_results (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL,
    solar_usage FLOAT,
    battery_usage FLOAT,
    grid_usage FLOAT,
    energy_saved FLOAT,
    cost_saved FLOAT,
    co2_reduced FLOAT
);
