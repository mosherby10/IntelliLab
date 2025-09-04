from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from .chunking import split_by_tokens
from .ingest import ingest_document
from .retriever import retrieve

router = APIRouter(prefix="/nlp", tags=["nlp"])
_MODEL = "distilbert-base-cased-distilled-squad"
qa_pipeline = pipeline("question-answering", model=_MODEL)

class QARequest(BaseModel):
    question: str
    context: str
    per_chunk_timeout_sec: float = 5.0

class IngestRequest(BaseModel):
    doc_id: str = "doc"
    text: str

@router.post("/qa")
def qa(req: QARequest):
    chunks = split_by_tokens(req.context)
    best = {"answer": None, "score": -1.0}
    with ThreadPoolExecutor(max_workers=1) as ex:
        for ch in chunks:
            try:
                res = ex.submit(qa_pipeline, question=req.question, context=ch).result(timeout=req.per_chunk_timeout_sec)
                if res["score"] > best["score"]:
                    best = res
            except TimeoutError: continue
    if best["score"] < 0: raise HTTPException(500, "QA failed")
    return best

@router.post("/ingest")
def ingest(req: IngestRequest):
    return {"chunks_added": ingest_document(req.text, req.doc_id)}

class RAGRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/ask_rag")
def ask_rag(req: RAGRequest):
    cands = retrieve(req.question, req.top_k)
    if not cands: raise HTTPException(404, "No data ingested")
    best = {"answer": None, "score": -1.0}
    for c in cands:
        res = qa_pipeline(question=req.question, context=c["text"])
        if res["score"] > best["score"]: best = res
    return best
