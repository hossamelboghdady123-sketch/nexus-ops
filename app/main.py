from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="NEXUS Ops",
    description="Cloud Reliability and DevSecOps Platform",
    version="0.1.0",
)

INDEX_FILE = Path(__file__).parent / "templates" / "index.html"


@app.get("/", response_class=HTMLResponse)
def root():
    return HTMLResponse(
        content=INDEX_FILE.read_text(encoding="utf-8")
    )


@app.get("/api")
def api_info():
    return {
        "service": "NEXUS Ops",
        "status": "running",
        "version": app.version,
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


Instrumentator().instrument(app).expose(app, endpoint="/metrics")
