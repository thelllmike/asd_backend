from fastapi import APIRouter, File, UploadFile, HTTPException
from model.tensorflow_model import predict_image
from shemas.cnn_prediction_shema import PredictionResponse

router = APIRouter()

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
