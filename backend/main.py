from __future__ import annotations

import time, logging
from pathlib import Path
from fastapi import FastAPI, Request, Response

from backend.logger import setup_logging
from backend.recommender_fp import FPGrowthRecommender
from backend.recommender_dl import DLRecommender

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Hybrid Recommender API", version="1.0.0")

fp_rec = FPGrowthRecommender(Path("data/rules.csv"))
dl_rec = DLRecommender(Path("models/ncf_model.pt"))

# middleware: log every request
@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = f"{request.method} {request.url.path}"
    t0   = time.perf_counter()
    response: Response = await call_next(request)
    logger.info("%s | %d | %.2f ms",
                idem, response.status_code, (time.perf_counter()-t0)*1000)
    return response

# API endpoints
@app.get("/recommend/by-item")
def rec_by_item(item: str, top_k: int = 5):

    logger.info("by‑item request item=%s top_k=%d", item, top_k)
    recs = fp_rec.recommend(item, top_k)
    return {"item": item, "suggestions": recs}

@app.get("/recommend/by-user")
def rec_by_user(user_id: int, top_k: int = 5):
    logger.info("by‑user request user_id=%s top_k=%d", user_id, top_k)
    recs = dl_rec.recommend(user_id, top_k)
    return {"user_id": user_id, "suggestions": recs}