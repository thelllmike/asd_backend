from fastapi import FastAPI
from db import engine, Base
from models.prediction_model import Prediction  # This registers your model
from routers.cnn_prediction import router as cnn_prediction_router
from routers.login_router import router as login_router
from routers import prediction

# This line creates all tables automatically if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASD Progress Prediction API")

app.include_router(prediction.router, prefix="/api", tags=["predictions"])
app.include_router(cnn_prediction_router, prefix="/api", tags=["predictions"])
app.include_router(login_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the ASD Progress Prediction API"}
