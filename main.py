from fastapi import FastAPI
from db import engine, Base
from models.prediction_model import Prediction  # This registers your model
from routers import prediction

# This line creates all tables automatically if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ASD Progress Prediction API")

app.include_router(prediction.router, prefix="/api", tags=["predictions"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the ASD Progress Prediction API"}
