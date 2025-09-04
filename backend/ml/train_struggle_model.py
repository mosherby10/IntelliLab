import json
from datetime import datetime
from sqlalchemy.orm import Session
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from app.database import SessionLocal
from ml.etl.features import build_training_table, feature_names
from .registry import save_model_with_metadata

def train_and_register():
    db: Session = SessionLocal()
    try:
        X, y, _ = build_training_table(db)
        if len(X) < 10:
            raise RuntimeError("Not enough data to train.")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=200)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "f1": float(f1_score(y_test, y_pred)),
        }
        meta = {
            "model_type": "LogisticRegression",
            "feature_names": feature_names(),
            "trained_at": datetime.utcnow().isoformat(),
            "metrics": metrics,
        }
        return save_model_with_metadata(model, meta)
    finally:
        db.close()

if __name__ == "__main__":
    out = train_and_register()
    print("Model trained and saved:", json.dumps(out, indent=2))
