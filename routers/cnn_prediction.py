from fastapi import APIRouter, File, UploadFile, HTTPException , Depends, Form
from sqlalchemy.orm import Session
from model.tensorflow_model import predict_image
# from shemas.cnn_prediction_shema import PredictionResponse
from models.cnn_prediction_model import ColoringPrediction
from shemas.cnn_prediction_shema import (
    ColoringPredictionCreate,
    ColoringPredictionResponse,
    PredictionResponse
)
from cruds.cnn_prediction_crud import create_coloring_prediction
from db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/predict_image", response_model=PredictionResponse)
async def predict_image_endpoint(file: UploadFile = File(...)):
    """
    Endpoint that receives an image file, runs the model prediction,
    and returns the predicted label and confidence.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided.")
    try:
        contents = await file.read()
        predicted_label, confidence = predict_image(contents)
        return PredictionResponse(predicted_label=predicted_label, confidence=confidence)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
    
#save predicted details

@router.post("/detect_and_save", response_model=ColoringPredictionResponse)
async def detect_and_save(
    file: UploadFile = File(...),
    user_id: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    1) Receives an image file + user_id, age, gender.
    2) Predicts the label & confidence using the CNN model.
    3) Saves the record to the DB.
    4) Returns the saved record.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No file provided.")
    try:
        image_bytes = await file.read()
        predicted_label, confidence = predict_image(image_bytes)

        # Prepare the data for saving
        prediction_data = ColoringPredictionCreate(
            user_id=user_id,
            age=age,
            gender=gender,
            predicted_label=predicted_label,
            confidence=confidence
        )

        # Save to the DB
        record = create_coloring_prediction(db, prediction_data)
        return record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

@router.get("/progress/{user_id}")
def get_progress(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve the two most recent predictions for a user (based on created_at timestamp) and calculate progress:
    
        progress = (score of second most recent prediction) - (score of newest prediction)
    
    Mapping:
        "asd_mild_coloring_3-6": 25
        "asd_moderate_coloring_3-6": 50
        "asd_severe_coloring_3-6": 75
        "asdwithcd_mild_coloring_3-6": 25
        "asdwithcd_moderate_coloring_3-6": 50
        "asdwithcd_severe_coloring_3-6": 75
        "non_asd_normal_coloring_3-6": 0
        
    For example, if the second most recent prediction is "asd_severe_coloring_3-6" (75)
    and the most recent is "asd_mild_coloring_3-6" (25), then progress = 75 - 25 = 50%.
    """
    # Query the two latest predictions sorted by created_at descending.
    predictions = (
        db.query(ColoringPrediction)
          .filter(ColoringPrediction.user_id == str(user_id))
          .order_by(ColoringPrediction.created_at.desc())
          .limit(2)
          .all()
    )
    
    if len(predictions) < 2:
        raise HTTPException(status_code=404, detail="Not enough predictions to calculate progress")
    
    # Most recent prediction (newest)
    newest = predictions[0]
    # Second most recent prediction (baseline)
    baseline = predictions[1]
    
    mapping = {
        "asd_mild_coloring_3-6": 25,
        "asd_moderate_coloring_3-6": 50,
        "asd_severe_coloring_3-6": 75,
        "asdwithcd_mild_coloring_3-6": 25,
        "asdwithcd_moderate_coloring_3-6": 50,
        "asdwithcd_severe_coloring_3-6": 75,
        "non_asd_normal_coloring_3-6": 0
    }
    
    baseline_score = mapping.get(baseline.predicted_label, 0)
    newest_score = mapping.get(newest.predicted_label, 0)
    
    # Calculate progress as the difference (baseline - newest).
    progress = baseline_score - newest_score
    
    return {
        "user_id": user_id,
        "progress_percentage": progress,
        "baseline_prediction": baseline.predicted_label,
        "followup_prediction": newest.predicted_label,
        "baseline_date": baseline.created_at,
        "followup_date": newest.created_at
    }
