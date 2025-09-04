import os, json, numpy as np
from typing import List, Dict
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer

STORE_DIR = os.path.join(os.path.dirname(__file__), "rag_store")
CHUNKS_PATH, EMB_PATH = os.path.join(STORE_DIR, "chunks.jsonl"), os.path.join(STORE_DIR, "embeddings.npy")
_EMB_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def _load_chunks() -> List[Dict]:
    if not os.path.exists(CHUNKS_PATH): return []
    return [json.loads(l) for l in open(CHUNKS_PATH, encoding="utf-8")]

def retrieve(query: str, top_k: int = 5) -> List[Dict]:
    chunks = _load_chunks()
    if not chunks or not os.path.exists(EMB_PATH): return []
    embs = np.load(EMB_PATH)
    qvec = _EMB_MODEL.encode([query], convert_to_numpy=True, normalize_embeddings=True)
    nn = NearestNeighbors(n_neighbors=min(top_k, len(embs)), metric="cosine").fit(embs)
    dists, idxs = nn.kneighbors(qvec)
    return [{"rank": i+1, "score": float(1-dists[0][i]), **chunks[idx]} for i, idx in enumerate(idxs[0])]
