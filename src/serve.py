
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache
import os

# Get the directory of this script and go up one level to find models
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "relevance_calibrator.joblib")

app = FastAPI()

class RequestItem(BaseModel):
    url: str | None = None
    snippet: str

# Load on startup
#MODEL = joblib.load('relevance_calibrator.joblib')
MODEL = joblib.load(MODEL_PATH)
EMB = SentenceTransformer('all-MiniLM-L6-v2')

@lru_cache(maxsize=20000)
def embed_text(text: str):
    return EMB.encode([text], convert_to_numpy=True)[0]

@app.post('/score')
def score(item: RequestItem):
    emb = embed_text(item.snippet)
    prob = MODEL.predict_proba([emb])[0,1]
    bid = int(prob >= 0.354374)
    price = 0.500000 + prob * (6.000000 - 0.500000)
    return {'bid': bid, 'price': round(price, 3), 'score': float(round(prob,4))}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
