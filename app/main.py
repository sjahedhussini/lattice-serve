from fastapi import FastAPI
from app.schemas import PredictRequest, PredictResponse
from app.logging_config import configure_logging, log
from models.stub import load_model
from prometheus_fastapi_instrumentator import Instrumentator
import time

app = FastAPI(title="Lattice Serve")
Instrumentator().instrument(app).expose(app)
configure_logging()

model = load_model()

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    start = time.perf_counter()
    score = model.predict_proba(request.features)
    duration_ms = (time.perf_counter() - start) * 1000
    
    log.info(
            "prediction",
            feature_count=len(request.features),
            score=score,
            duration_ms=round(duration_ms, 2),
            model_version=model.version 
    )

    return PredictResponse(
            fraud_probability=score,
            model_version=model.version,
            )


@app.get("/health")
def health():
    return {
        "status":"ok",
        "model_loaded": model is not None,
        "model_version": model.version,
    }


