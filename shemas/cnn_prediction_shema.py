from pydantic import BaseModel
from datetime import datetime

class PredictionResponse(BaseModel):
    predicted_label: str
    confidence: float


class ColoringPredictionCreate(BaseModel):
    user_id: str
    age: int
    gender: str
    predicted_label: str
    confidence: float

class ColoringPredictionResponse(BaseModel):
    id: int
    user_id: str
    age: int
    gender: str
    predicted_label: str
    confidence: float
    created_at: datetime

    class Config:
        orm_mode = True