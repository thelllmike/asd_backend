from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shemas.prediction_shema import PredictionCreate, PredictionResponse, OverallPredictionResponse
from cruds.prediction_crud import create_prediction, get_predictions_by_user
from db import SessionLocal
import joblib
import numpy as np
from collections import Counter

router = APIRouter()

# Load the pre-trained model (ensure it supports predict_proba)
model = joblib.load("asd_progress_model.pkl")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict", response_model=PredictionResponse)
def create_prediction_endpoint(prediction: PredictionCreate, db: Session = Depends(get_db)):
    feature_columns = [
        "Eye_Contact_Initial", "Follows_Instructions_Initial", "Verbal_Improvement_Initial", 
        "Repeats_Words_Initial", "Routine_Sensitivity_Initial", "Repetitive_Actions_Initial", 
        "Focus_On_Objects_Initial", "Social_Interaction_Initial", "Outdoor_Change_Initial", 
        "Therapy_Engagement_Initial", "Eye_Contact_Followup", "Follows_Instructions_Followup", 
        "Verbal_Improvement_Followup", "Repeats_Words_Followup", "Routine_Sensitivity_Followup", 
        "Repetitive_Actions_Followup", "Focus_On_Objects_Followup", "Social_Interaction_Followup", 
        "Outdoor_Change_Followup", "Therapy_Engagement_Followup"
    ]
    
    # Build the feature array
    features = np.array([getattr(prediction, col) for col in feature_columns]).reshape(1, -1)
    
    # Get prediction probabilities and calculate improvement percentage
    probabilities = model.predict_proba(features)[0]
    improvement_percentage = probabilities[1] * 100  # Assuming index 1 is for 'improved'
    predicted_label = int(model.predict(features)[0])
    
    # Save to DB with improvement_percentage
    db_prediction = create_prediction(
        db=db,
        prediction=prediction,
        predicted_label=predicted_label,
        improvement_percentage=improvement_percentage
    )
    
    response_data = {
        "id": db_prediction.id,
        "user_id": db_prediction.user_id,
        "prediction": db_prediction.prediction,
        "improvement_percentage": db_prediction.improvement_percentage,
        "created_at": db_prediction.created_at
    }
    return response_data

@router.get("/user/{user_id}", response_model=OverallPredictionResponse)
def get_overall_prediction(user_id: str, db: Session = Depends(get_db)):
    predictions = get_predictions_by_user(db=db, user_id=user_id)
    if not predictions:
        raise HTTPException(status_code=404, detail="No predictions found for this user.")
    
    # Compute overall prediction as the mode of prediction labels
    prediction_labels = [pred.prediction for pred in predictions]
    overall_prediction = Counter(prediction_labels).most_common(1)[0][0]
    
    # Compute overall improvement percentage as the average of all stored improvement percentages
    improvement_percentages = [pred.improvement_percentage for pred in predictions if pred.improvement_percentage is not None]
    overall_improvement_percentage = sum(improvement_percentages) / len(improvement_percentages) if improvement_percentages else 0
    
    return OverallPredictionResponse(
        user_id=user_id,
        overall_prediction=overall_prediction,
        count=len(predictions),
        overall_improvement_percentage=overall_improvement_percentage
    )
