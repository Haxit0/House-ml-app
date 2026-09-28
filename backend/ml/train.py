from pathlib import Path
import json
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# Paths
BASE_DIR = Path(__file__).resolve().parent
ARTIFACTS_DIR = BASE_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = ARTIFACTS_DIR / "model_latest.joblib"
METRICS_PATH = ARTIFACTS_DIR / "metrics_latest.json"

# Generate synthetic data
rng = np.random.default_rng(42)
n_samples = 1000

area_sqft = rng.normal(1500, 500, n_samples).clip(300, 4000)
bedrooms = rng.integers(1, 6, n_samples)
bathrooms = rng.integers(1, 4, n_samples)
location_score = rng.integers(1, 11, n_samples)
age_years = rng.integers(0, 80, n_samples)

X = np.column_stack(
    [area_sqft, bedrooms, bathrooms, location_score, age_years]
)

y = (
    area_sqft * 250
    + bedrooms * 50000
    + bathrooms * 30000
    + location_score * 80000
    - age_years * 1000
)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

metrics = {
    "mae": mean_absolute_error(y_test, y_pred),
    "rmse": mean_squared_error(y_test, y_pred) ** 0.5,
    "r2": r2_score(y_test, y_pred),
}

# Save artifacts
joblib.dump(model, MODEL_PATH)
with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=2)

print("Model saved to:", MODEL_PATH)
print("Metrics:", metrics)
