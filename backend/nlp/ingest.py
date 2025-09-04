import os, json, numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from .chunking import split_by_tokens

STORE_DIR = os.path.join(os.path.dirname(__file__), "rag_store")
os.makedirs(STORE_DIR, exist_ok=True)
CHUNKS_PATH, EMB_PATH = os.path.join(STORE_DIR, "chunks.jsonl"), os.path.join(STORE_DIR, "embeddings.npy")
_EMB_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def _append_jsonl(path: str, rows: List[Dict]):
    with open(path, "a", encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r) + "\n")

def ingest_document(text: str, doc_id: str = "doc") -> int:
    chunks = split_by_tokens(text)
    rows = [{"doc_id": doc_id, "chunk_id": i, "text": ch} for i, ch in enumerate(chunks)]
    _append_jsonl(CHUNKS_PATH, rows)
    embs = _EMB_MODEL.encode([r["text"] for r in rows], convert_to_numpy=True, normalize_embeddings=True)
    if os.path.exists(EMB_PATH):
        old = np.load(EMB_PATH)
        embs = np.vstack([old, embs])
    np.save(EMB_PATH, embs)
    return len(rows)
