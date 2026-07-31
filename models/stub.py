import numpy as np 

class StubModel:
    version = "0.0.1-stub"

    def predict_proba(self, features: list[float]) -> float:
        total = np.sum(features)
        return float(1/(1+np.exp(-total)))


def load_model():
    return StubModel()
