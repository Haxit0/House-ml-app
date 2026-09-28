from pathlib import Path
import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

# 5 input features:
# area_sqft, bedrooms, bathrooms, location_score, age_years
X = np.random.rand(200, 5)
y = (
    X[:, 0] * 300
    + X[:, 1] * 50
    + X[:, 2] * 40
    + X[:, 3] * 80
    + (1 - X[:, 4]) * 30
) * 1000

model = LinearRegression()
model.fit(X, y)

out_dir = Path(__file__).resolve().parent / "artifacts"
out_dir.mkdir(parents=True, exist_ok=True)

out_path = out_dir / "model_latest.joblib"
joblib.dump(model, out_path)

print("Saved model to:", out_path)
