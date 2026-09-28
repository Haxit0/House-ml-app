from fastapi import FastAPI
from .schemas import HouseInput, PredictionResponse, FeedbackInput
from .predict import load_model, predict_price
from .db import init_db, get_connection
from .metrics import load_metrics
from .retrain import retrain_model
from fastapi.middleware.cors import CORSMiddleware
from .history import load_prediction_history




app = FastAPI(title="House Price Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()
    load_model()


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics")
def metrics():
    data = load_metrics()
    if data is None:
        return {"error": "Metrics not available"}
    return data


@app.post("/predict", response_model=PredictionResponse)
def predict(input_data: HouseInput):
    price = predict_price(input_data.dict())
    return {"predicted_price": price}

@app.post("/feedback")
def feedback(data: FeedbackInput):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (
            area_sqft, bedrooms, bathrooms,
            location_score, age_years, actual_price, predicted_price
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.area_sqft,
            data.bedrooms,
            data.bathrooms,
            data.location_score,
            data.age_years,
            data.actual_price,
            data.predicted_price,
        ),
    )

    conn.commit()
    conn.close()

    return {"message": "Feedback stored"}

@app.post("/retrain")
def retrain():
    result = retrain_model()
    load_model()
    return result

@app.get("/history")
def history():
    return load_prediction_history()