from pydantic import BaseModel, Field, ValidationError
from typing import List, Dict, Any
from .registry import load_latest_model

# 1. Define input schema
class StruggleFeatures(BaseModel):
    last_quiz_score: float = Field(..., ge=0, le=100, description="Most recent quiz score (0-100)")
    avg_submission_score: float = Field(..., ge=0, le=100, description="Average score of submissions (0-100)")
    submissions_count: int = Field(..., ge=0, description="Total number of submissions")
    inactive_days: float = Field(..., ge=0, description="Days since last activity")
    avg_session_minutes: float = Field(..., ge=0, description="Average time spent per session (minutes)")

    # 🔹 New enriched features
    quiz_trend: float = Field(..., description="Difference between last and previous quiz scores")
    submission_success_rate: float = Field(..., ge=0, le=1, description="Proportion of submissions with passing scores")
    score_variance: float = Field(..., ge=0, description="Variance in submission scores")

# 2. Convert payload to feature vector
def _to_vector(payload: StruggleFeatures, feature_names: List[str]) -> List[float]:
    d = payload.dict()
    missing = [f for f in feature_names if f not in d]
    if missing:
        raise ValueError(f"Missing features required by model: {missing}")
    return [float(d[name]) for name in feature_names]

# 3. Lazy-load the latest model
_model, _meta, _ver = None, None, None

def get_model():
    global _model, _meta, _ver
    if _model is None:
        _model, _meta, _ver = load_latest_model()
    return _model, _meta, _ver

# 4. Prediction function with validation
def predict_proba(payload: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Validate against schema
        data = StruggleFeatures(**payload)
    except ValidationError as e:
        return {"error": e.errors()}

    model, meta, ver = get_model()
    feats = _to_vector(data, meta["feature_names"])
    X = [feats]

    pred = int(model.predict(X)[0])
    proba = float(model.predict_proba(X)[0][1]) if hasattr(model, "predict_proba") else None

    return {
        "version": ver,
        "features": data.dict(),
        "prediction": pred,
        "probability_struggling": proba
    }
