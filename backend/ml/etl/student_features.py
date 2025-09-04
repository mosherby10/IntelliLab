# backend/ml/etl/student_features.py
from datetime import datetime
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, Submission
import numpy as np


def _days_between(d1, d2) -> int:
    """Helper to compute days between two datetimes."""
    return max(0, (d2 - d1).days) if d1 and d2 else 9999


def build_student_feature_row(db: Session, user_id: int) -> Tuple[List[float], Dict]:
    """
    Extracts a single student's features from the database.
    Returns (feature_vector, auxiliary_info).
    """

    # Get last submission (for last_quiz_score)
    last_sub = (
        db.query(Submission)
        .filter(Submission.user_id == user_id, Submission.score != None)
        .order_by(Submission.created_at.desc())
        .first()
    )
    last_quiz_score = float(last_sub.score) if last_sub else 0.0

    # Average submission score
    avg_score = (
        db.query(func.avg(Submission.score))
        .filter(Submission.user_id == user_id, Submission.score != None)
        .scalar()
    )
    avg_submission_score = float(avg_score) if avg_score else 0.0

    # Count of submissions
    submissions_count = (
        db.query(func.count(Submission.id))
        .filter(Submission.user_id == user_id)
        .scalar()
        or 0
    )

    # Last submission date → inactivity
    last_date = (
        db.query(func.max(Submission.created_at))
        .filter(Submission.user_id == user_id)
        .scalar()
    )
    now = datetime.utcnow()
    inactive_days = float(_days_between(last_date, now))

    # Placeholder (to be filled when we track sessions)
    avg_session_minutes = 0.0

    # --- NEW FEATURES ---

    # Quiz trend: slope of scores over time
    subs = (
        db.query(Submission.score, Submission.created_at)
        .filter(Submission.user_id == user_id, Submission.score != None)
        .order_by(Submission.created_at.asc())
        .all()
    )
    quiz_trend = 0.0
    if len(subs) > 1:
        scores = [float(s[0]) for s in subs]
        times = np.arange(len(scores))
        slope, _ = np.polyfit(times, scores, 1)
        quiz_trend = float(slope)

    # Submission success rate: fraction with score ≥ 50
    success_rate = 0.0
    if submissions_count > 0:
        passed = (
            db.query(func.count(Submission.id))
            .filter(Submission.user_id == user_id, Submission.score >= 50)
            .scalar()
        )
        success_rate = float(passed) / submissions_count

    # Score variance
    score_variance = 0.0
    if len(subs) > 1:
        scores = [float(s[0]) for s in subs]
        score_variance = float(np.var(scores))

    # --- Feature vector ---
    features = [
        last_quiz_score,
        avg_submission_score,
        float(submissions_count),
        inactive_days,
        avg_session_minutes,
        quiz_trend,
        success_rate,
        score_variance,
    ]

    aux = {
        "user_id": user_id,
        "last_quiz_score": last_quiz_score,
        "avg_submission_score": avg_submission_score,
        "submissions_count": submissions_count,
        "inactive_days": inactive_days,
        "avg_session_minutes": avg_session_minutes,
        "quiz_trend": quiz_trend,
        "submission_success_rate": success_rate,
        "score_variance": score_variance,
    }

    return features, aux


def build_training_table(db: Session) -> Tuple[List[List[float]], List[int], List[Dict]]:
    """
    Build training dataset: features (X), labels (y), and raw rows.
    """
    X, y, rows = [], [], []
    users = db.query(User.id).all()
    for (user_id,) in users:
        feats, info = build_student_feature_row(db, user_id)
        # Label: struggling if avg score < 60 or inactive for >14 days
        struggling = int(info["avg_submission_score"] < 60.0 or info["inactive_days"] > 14)
        X.append(feats)
        y.append(struggling)
        rows.append(info)
    return X, y, rows


def feature_names() -> List[str]:
    """Return feature names in order."""
    return [
        "last_quiz_score",
        "avg_submission_score",
        "submissions_count",
        "inactive_days",
        "avg_session_minutes",
        "quiz_trend",
        "submission_success_rate",
        "score_variance",
    ]
