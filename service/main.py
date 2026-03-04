from fastapi import FastAPI, HTTPException
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import os

app = FastAPI()

reqs = Counter("recommend_requests_total", "requests", ["status"])
lat = Histogram("recommend_latency_seconds", "latency")

@app.get("/healthz")
def healthz():
    return {"status": "ok", "version": os.getenv("MODEL_VERSION", "v0.1")}

@app.get("/")
def root():
    return {"message": "Server running. Use /docs, /healthz, /recommend/{user_id}, /metrics"}

@app.get("/recommend/{user_id}")
@lat.time()
def recommend(user_id: int, k: int = 5):
    try:
        movies = [50, 172, 1, 20, 10]
        reqs.labels("200").inc()
        return movies[:k]
    except Exception as e:
        reqs.labels("500").inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}