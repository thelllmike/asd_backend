from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from db import Base

class ColoringPrediction(Base):
    __tablename__ = "coloring_predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    age = Column(Integer)
    gender = Column(String(10))
    predicted_label = Column(String(255))
    confidence = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
