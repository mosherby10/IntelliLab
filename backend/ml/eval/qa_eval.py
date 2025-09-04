import json, re
from ..nlp.router import qa_pipeline

def normalize(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()

def f1(pred: str, truth: str) -> float:
    p, t = normalize(pred).split(), normalize(truth).split()
    if not p or not t: return 0.0
    common = sum(min(p.count(w), t.count(w)) for w in set(p))
    if not common: return 0.0
    prec, rec = common / len(p), common / len(t)
    return 2 * prec * rec / (prec + rec)

def run_eval(path: str):
    data = json.load(open(path))
    scores = [f1(qa_pipeline(question=x["question"], context=x["context"])["answer"], x["answer"]) for x in data]
    print("Avg F1:", sum(scores)/len(scores))

if __name__ == "__main__":
    run_eval("backend/app/ml/eval/qa_small.json")
