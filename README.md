# House Price ML App

A small full-stack project for exploring house price prediction. A FastAPI service trains a random forest on generated housing data, serves predictions, stores actual sale prices as feedback, and tracks model performance. The React frontend is intended to provide a form and metrics dashboard.

> **Project status:** The API can be run from the files in this repository. The frontend currently imports `src/components/predictionForm` and `src/components/MetricsDashboard`, but those component files are missing. Its development server may start, but the page will not render until the components are added.

## What it does

- Predicts a price from floor area, bedroom and bathroom counts, location score, and property age.
- Saves submitted actual prices and the corresponding predictions in SQLite.
- Retrains a 200-tree random forest using generated data plus saved feedback.
- Exposes the latest MAE, RMSE, and R² scores, model metric history, and feedback history through the API.

**The training data is synthetic.** The generated target follows a simple formula, so the predictions and metrics demonstrate the workflow rather than real market accuracy. No currency or geographic market is defined.

## Tech stack

| Part | Technology |
| --- | --- |
| API | Python, FastAPI, Uvicorn, Pydantic |
| Model | scikit-learn, NumPy, joblib |
| Storage | SQLite (`backend/feedback.db`) |
| Frontend | React, Vite, Recharts |

## Run the API locally

You need Python 3 and a terminal at the repository root. Create a virtual environment, install dependencies, and train the initial model:

```bash
python -m venv .venv
```

Activate it with `.venv\Scripts\Activate.ps1` in PowerShell, or `source .venv/bin/activate` on macOS/Linux. Then run:

```bash
python -m pip install -r backend/requirements.txt
python -m backend.ml.train
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

The API is available at `http://127.0.0.1:8000`, with interactive documentation at [`/docs`](http://127.0.0.1:8000/docs). Training creates `backend/ml/artifacts/model_latest.joblib` and `metrics_latest.json`. The API loads the model on startup, so run the training command before starting the server.

## Try a prediction

Open `/docs`, expand **POST /predict**, and use this example request:

```json
{
  "area_sqft": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "location_score": 7,
  "age_years": 15
}
```

The response contains a numeric `predicted_price`. The inputs have these limits:

| Field | Meaning | Accepted value |
| --- | --- | --- |
| `area_sqft` | Floor area in square feet | Greater than 0 |
| `bedrooms` | Bedroom count | Integer, 0 or more |
| `bathrooms` | Bathroom count | Integer, 0 or more |
| `location_score` | Relative location rating | 1 to 10 |
| `age_years` | Property age in years | Integer, 0 or more |

## API routes

| Method | Route | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Check that the API is running. |
| `POST` | `/predict` | Return `predicted_price` for the five house features. |
| `POST` | `/feedback` | Save the five features, `predicted_price`, and a positive `actual_price`. |
| `POST` | `/retrain` | Train a new model from synthetic data and saved feedback; return its version and metrics. |
| `GET` | `/metrics` | Return the latest metrics and retraining history. |
| `GET` | `/history` | Return saved feedback records, newest first, with `error = actual_price - predicted_price`. |

`/feedback` stores the prediction value supplied in the request; it does not calculate that value itself. The initial training script writes the latest metrics, while `/retrain` also appends an entry to `metrics_history.json` and saves a versioned model.

## Frontend

The frontend is configured to run at `http://127.0.0.1:3000` and call the API at `http://127.0.0.1:8000`. The API's CORS configuration allows that exact frontend origin. Once the missing components are added, start it in a second terminal:

```bash
cd frontend
npm ci
npm run dev
```

Until then, use the API's `/docs` page to try the working backend.

## Project layout

```text
backend/
  app/             FastAPI routes, schemas, SQLite access, prediction, retraining
  ml/              Training scripts and generated model artifacts
  requirements.txt Python dependencies
frontend/
  src/             React entry point, API helpers, and styles
  package.json     Frontend dependencies and scripts
```

The trained model files are generated locally by the training commands. `backend/feedback.db` holds feedback submitted to the API.
