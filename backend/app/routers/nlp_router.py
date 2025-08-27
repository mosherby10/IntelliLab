# backend/app/routers/nlp_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter(prefix="/nlp", tags=["nlp"])

# Create a question-answering pipeline using a small SQuAD model.
# NOTE: this may require PyTorch or TensorFlow to be installed in the environment.
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

class QARequest(BaseModel):
    question: str
    context: str

@router.post("/qa")
def answer_qa(req: QARequest):
    """
    Accepts a question and a context (text) and returns an answer span from the context.
    """
    result = qa_pipeline(question=req.question, context=req.context)
    return {"answer": result.get("answer"), "score": float(result.get("score", 0.0))}
