# backend/app/routers/ml_router.py
from fastapi import APIRouter, HTTPException
from ml.predict import predict_proba, StruggleFeatures

router = APIRouter(prefix="/ml", tags=["ML"])

@router.post("/predict")
def predict_student_struggle(features: StruggleFeatures):
    """
    Predict if a student is struggling based on recent activity.
    """
    try:
        result = predict_proba(features.dict())  # 👈 FIXED: convert to dict
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
