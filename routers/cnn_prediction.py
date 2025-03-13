from fastapi import APIRouter, File, UploadFile, HTTPException , Depends, Form
from sqlalchemy.orm import Session
from model.tensorflow_model import predict_image
# from shemas.cnn_prediction_shema import PredictionResponse
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
