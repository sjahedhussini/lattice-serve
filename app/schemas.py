from pydantic import BaseModel

class PredictRequest(BaseModel):
    features: list[float]

class PredictResponse(BaseModel):
    fraud_probability: float
    model_version: str
