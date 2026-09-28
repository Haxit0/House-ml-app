from pathlib import Path
import json
import joblib
import sqlite3
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from .db import DB_PATH


BASE_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = BASE_DIR / "ml" / "artifacts"
ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


MODEL_LATEST = ARTIFACTS_DIR / "model_latest.joblib"
METRICS_LATEST = ARTIFACTS_DIR / "metrics_latest.json"


def load_feedback():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT area_sqft, bedrooms, bathrooms,
               location_score, age_years, actual_price
        FROM feedback
        """
    )

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return None

    data = np.array(rows)
    return data[:, :5], data[:, 5]


def retrain_model():
    # ----- load original synthetic data -----
    version = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    version_readable = datetime.utcnow().isoformat()
    rng = np.random.default_rng(42)
    n_samples = 1000

    area_sqft = rng.normal(1500, 500, n_samples).clip(300, 4000)
    bedrooms = rng.integers(1, 6, n_samples)
    bathrooms = rng.integers(1, 4, n_samples)
    location_score = rng.integers(1, 11, n_samples)
    age_years = rng.integers(0, 80, n_samples)

    X_orig = np.column_stack(
        [area_sqft, bedrooms, bathrooms, location_score, age_years]
    )

    y_orig = (
        area_sqft * 250
        + bedrooms * 50000
        + bathrooms * 30000
        + location_score * 80000
        - age_years * 1000
    )

    # ----- load feedback -----
    feedback = load_feedback()
    if feedback is not None:
        X_fb, y_fb = feedback
        X = np.vstack([X_orig, X_fb])
        y = np.concatenate([y_orig, y_fb])
    else:
        X, y = X_orig, y_orig
    

    # ----- train/test split -----
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    metrics = {
        "mae": mean_absolute_error(y_test, y_pred),
        "rmse": mean_squared_error(y_test, y_pred) ** 0.5,
        "r2": r2_score(y_test, y_pred),
    }

    HISTORY_PATH = ARTIFACTS_DIR / "metrics_history.json"

    # Load existing history
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f)
    else:
        history = []

    history.append({
    "version": version,
    "n_estimators": 200,
    **metrics
    })


    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


    # ----- versioning -----
    versioned_model = ARTIFACTS_DIR / f"model_{version}.joblib"

    joblib.dump(model, versioned_model)
    joblib.dump(model, MODEL_LATEST)

    with open(METRICS_LATEST, "w") as f:
        json.dump(metrics, f, indent=2)

    return {
        "version": version,
        "version_readable": version_readable,
        "metrics": metrics,
    }
