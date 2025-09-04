from typing import List
from transformers import AutoTokenizer

_MODEL_NAME = "distilbert-base-cased-distilled-squad"
_tokenizer = AutoTokenizer.from_pretrained(_MODEL_NAME)

def split_by_tokens(text: str, max_tokens: int = 350, overlap: int = 50) -> List[str]:
    if not text: return []
    tokens = _tokenizer.encode(text, add_special_tokens=False)
    chunks, start = [], 0
    while start < len(tokens):
        end = min(start + max_tokens, len(tokens))
        chunk = _tokenizer.decode(tokens[start:end])
        chunks.append(chunk)
        if end == len(tokens): break
        start = max(0, end - overlap)
    return chunks
