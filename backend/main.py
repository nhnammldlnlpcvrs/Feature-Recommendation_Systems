import time
import logging
from pathlib import Path
from fastapi import FastAPI, Request, Response

from backend.logger import setup_logging
from backend.recommender_fp import FPGrowthRecommender
from backend.recommender_dl import DLRecommender

# set up logging
setup_logging()
logger = logging.getLogger(__name__)

# Init FastAPI
app = FastAPI(
    title="Hybrid Recommender API",
    version="1.0.0",
    description="A hybrid recommendation system using FP-Growth Algorithm and Deep Learning Models"
)

fp_rec = FPGrowthRecommender(Path("data/rules.csv"))
dl_rec = DLRecommender(Path("models/ncf_model.pt"))

# middleware: log every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s | Status: %d | %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        process_time
    )
    return response

# API endpoints
@app.get("/recommend/by-item")
def rec_by_item(item: str, top_k: int = 5):
    """
    Recommend similar items based on FP-Growth association rules.
    """
    logger.info("by‑item request item=%s top_k=%d", item, top_k)
    recs = fp_rec.recommend(item, top_k)
    
    return {"item": item, "suggestions": recs}

@app.get("/recommend/by-user")
def rec_by_user(user_id: int, top_k: int = 5):
    """
    Recommend items for a specific user using Deep Learning collaborative filtering.
    """
    logger.info("by‑user request user_id=%s top_k=%d", user_id, top_k)
    recs = dl_rec.recommend(user_id, top_k)
    
    return {"user_id": user_id, "suggestions": recs}