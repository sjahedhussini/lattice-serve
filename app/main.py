from fastapi import FastAPI
from app.schemas import PredictRequest, PredictResponse
from models.stub import load_model

app = FastAPI(title="Lattice Serve")
model = load_model()

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    score = model.predict_proba(request.features)
    return PredictResponse(
            fraud_probability=score,
            model_version=model.version,
            )
