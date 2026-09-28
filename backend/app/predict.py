from pathlib import Path
import joblib
import numpy as np

MODEL_PATH = Path(__file__).resolve().parents[1] / "ml" / "artifacts" / "model_latest.joblib"

_model = None


def load_model():
    global _model
    print("Looking for model at:", MODEL_PATH)

    if not MODEL_PATH.exists():
        print("Model file not found.")
        _model = None
        return

    _model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")


def predict_price(features: dict) -> float:
    if _model is None:
        raise RuntimeError("Model not loaded")

    X = np.array([[
        features["area_sqft"],
        features["bedrooms"],
        features["bathrooms"],
        features["location_score"],
        features["age_years"],
    ]])

    prediction = _model.predict(X)
    return float(prediction[0])
