from sqlalchemy.orm import Session
from models.cnn_prediction_model import ColoringPrediction
from shemas.cnn_prediction_shema import ColoringPredictionCreate

def create_coloring_prediction(db: Session, prediction_data: ColoringPredictionCreate):
    db_prediction = ColoringPrediction(
        user_id=prediction_data.user_id,
        age=prediction_data.age,
        gender=prediction_data.gender,
        predicted_label=prediction_data.predicted_label,
        confidence=prediction_data.confidence
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction
