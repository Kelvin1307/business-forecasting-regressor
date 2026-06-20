import os
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "regression_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "scaler.pkl")

model = None
scaler = None


def load_artifacts():
    """Load model and scaler artifacts into module-level variables.

    Raises RuntimeError if artifacts are missing.
    """
    global model, scaler

    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        raise RuntimeError("Model artifacts not found. Train the model first.")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)


def ensure_loaded():
    if model is None or scaler is None:
        load_artifacts()


def predict_budget(tv_budget: float, radio_budget: float, digital_budget: float) -> float:
    """Return predicted sales for the given budgets.

    Example: predict_budget(150.0, 30.0, 25.0)
    """
    ensure_loaded()
    features = [[tv_budget, radio_budget, digital_budget]]
    scaled = scaler.transform(features)
    prediction = model.predict(scaled)
    return float(prediction[0])
