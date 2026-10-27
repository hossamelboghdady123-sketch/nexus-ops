from datetime import datetime, timezone

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="NEXUS Ops",
    description="Cloud Reliability and DevSecOps Platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "service": "NEXUS Ops",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


Instrumentator().instrument(app).expose(app, endpoint="/metrics")
