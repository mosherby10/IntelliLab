# backend/app/routers/ml_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import os

router = APIRouter(prefix="/ml", tags=["ml"])

# Load model on import (simple approach)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml_models", "model.pkl")
MODEL_PATH = os.path.abspath(MODEL_PATH)

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

class PredictRequest(BaseModel):
    features: list  # list of numeric features

@router.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not available. Train and save first.")
    # convert list to 2D array for scikit-learn
    X = [req.features]
    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max() if hasattr(model, "predict_proba") else None
    return {"prediction": int(pred), "probability": float(prob) if prob is not None else None}
