import time
import logging
from pathlib import Path
from fastapi import FastAPI, Request, Response

from backend.logger import setup_logging
from backend.recommender_fp import FPGrowthRecommender
from backend.recommender_dl import DLRecommender

# setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Hybrid Recommender API",
    version="1.0.0",
    description="A hybrid recommendation system using FP-Growth Algorithms and Deep Learning (NCF)"
)

# Load FP-Growth rules
fp_rec = FPGrowthRecommender(Path("data/rules.csv"))

# Load Deep Learning model safely
try:
    dl_rec = DLRecommender(Path("models/ncf_model.pt"))
except Exception as e:
    logger.warning(f"Could not load DL model: {e}")
    dl_rec = None  # fallback if model missing

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration = (time.perf_counter() - start) * 1000
    logger.info("%s %s | %d | %.2f ms", request.method, request.url.path, response.status_code, duration)
    return response

@app.get("/health")
def health():
    return {"status": "ok", "message": "API is running"}

@app.get("/recommend/by-item")
def rec_by_item(item: str, top_k: int = 5):
    logger.info(f"by-item request: item={item}, top_k={top_k}")
    recs = fp_rec.recommend(item, top_k)
    return {"input": item, "type": "item-based", "results": recs}

@app.get("/recommend/by-user")
def rec_by_user(user_id: int, top_k: int = 5):
    logger.info(f"by-user request: user_id={user_id}, top_k={top_k}")
    if dl_rec is None:
        return {"error": "Deep Learning model not loaded"}
    recs = dl_rec.recommend(user_id, top_k)
    return {"input": user_id, "type": "user-based", "results": recs}