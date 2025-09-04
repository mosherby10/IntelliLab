from datetime import datetime
from typing import Dict, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, Submission


def _days_between(d1, d2) -> int:
    return max(0, (d2 - d1).days) if d1 and d2 else 9999


def build_student_feature_row(db: Session, user_id: int) -> Tuple[List[float], Dict]:
    # --- Basic features ---
    last_sub = (
        db.query(Submission)
        .filter(Submission.user_id == user_id, Submission.score != None)
        .order_by(Submission.created_at.desc())
        .first()
    )
    last_quiz_score = float(last_sub.score) if last_sub and last_sub.score is not None else 0.0

    avg_score = (
        db.query(func.avg(Submission.score))
        .filter(Submission.user_id == user_id, Submission.score != None)
        .scalar()
    )
    avg_submission_score = float(avg_score) if avg_score is not None else 0.0

    submissions = (
        db.query(Submission.score, Submission.created_at)
        .filter(Submission.user_id == user_id, Submission.score != None)
        .all()
    )
    submissions_count = len(submissions)

    last_date = max((s.created_at for s in submissions), default=None)
    now = datetime.utcnow()
    inactive_days = float(_days_between(last_date, now))

    avg_session_minutes = 0.0  # placeholder until we track sessions

    # --- Extra features ---
    scores = [s.score for s in submissions if s.score is not None]

    quiz_trend = last_quiz_score - avg_submission_score if submissions_count > 0 else 0.0
    submission_success_rate = (
        sum(1 for s in scores if s >= 60) / submissions_count if submissions_count > 0 else 0.0
    )
    score_variance = (max(scores) - min(scores)) if len(scores) > 1 else 0.0

    # --- Final feature vector ---
    features = [
        last_quiz_score,
        avg_submission_score,
        float(submissions_count),
        inactive_days,
        avg_session_minutes,
        quiz_trend,
        submission_success_rate,
        score_variance,
    ]

    # --- Auxiliary info (for debugging / inspection) ---
    aux = {
        "user_id": user_id,
        "last_quiz_score": last_quiz_score,
        "avg_submission_score": avg_submission_score,
        "submissions_count": submissions_count,
        "inactive_days": inactive_days,
        "avg_session_minutes": avg_session_minutes,
        "quiz_trend": quiz_trend,
        "submission_success_rate": submission_success_rate,
        "score_variance": score_variance,
    }

    return features, aux


def build_training_table(db: Session) -> Tuple[List[List[float]], List[int], List[Dict]]:
    X, y, rows = [], [], []
    users = db.query(User.id).all()
    for (user_id,) in users:
        feats, info = build_student_feature_row(db, user_id)

        # Label rule (still synthetic until we get real feedback)
        struggling = int(info["avg_submission_score"] < 60.0 or info["inactive_days"] > 14)

        X.append(feats)
        y.append(struggling)
        rows.append(info)
    return X, y, rows


def feature_names() -> List[str]:
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
