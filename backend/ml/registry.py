import os, json, joblib
from datetime import datetime
from typing import Dict, Tuple, Any

REG_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(REG_DIR, exist_ok=True)

def _timestamp() -> str:
    return datetime.utcnow().strftime("%Y%m%d-%H%M%S")

def save_model_with_metadata(model: Any, metadata: Dict) -> Dict:
    ver = _timestamp()
    model_path = os.path.join(REG_DIR, f"model-{ver}.pkl")
    meta_path  = os.path.join(REG_DIR, f"model-{ver}.json")
    joblib.dump(model, model_path)
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    with open(os.path.join(REG_DIR, "LATEST"), "w") as f:
        f.write(ver)
    return {"version": ver, "model_path": model_path, "meta_path": meta_path}

def load_latest_model() -> Tuple[Any, Dict, str]:
    latest_file = os.path.join(REG_DIR, "LATEST")
    if not os.path.exists(latest_file):
        raise FileNotFoundError("No model registered yet. Train first.")
    with open(latest_file) as f:
        ver = f.read().strip()
    model_path = os.path.join(REG_DIR, f"model-{ver}.pkl")
    meta_path  = os.path.join(REG_DIR, f"model-{ver}.json")
    model = joblib.load(model_path)
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    return model, meta, ver
