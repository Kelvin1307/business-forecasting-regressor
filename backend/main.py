import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
from .schemas import BudgetRequest

app = FastAPI(
    title="Business Forecasting Regressor",
    description="Predict sales from TV, Radio, and Digital advertising budgets.",
    version="1.0.0",
)

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "regression_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "scaler.pkl")

model = None
scaler = None


def load_artifacts():
    global model, scaler

    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise RuntimeError("Model artifacts not found. Train the model first.")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)


@app.on_event("startup")
def startup_event():
    load_artifacts()


@app.post("/predict/")
def predict(request: BudgetRequest):
    try:
        features = [[request.tv_budget, request.radio_budget, request.digital_budget]]
        scaled = scaler.transform(features)
        prediction = model.predict(scaled)
        return {"predicted_sales": float(prediction[0])}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
