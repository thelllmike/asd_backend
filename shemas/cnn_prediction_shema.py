from pydantic import BaseModel

class PredictionResponse(BaseModel):
    predicted_label: str
    confidence: float
