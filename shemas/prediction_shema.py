from pydantic import BaseModel
from datetime import datetime

class PredictionCreate(BaseModel):
    user_id: int
    Eye_Contact_Initial: float
    Follows_Instructions_Initial: float
    Verbal_Improvement_Initial: float
    Repeats_Words_Initial: float
    Routine_Sensitivity_Initial: float
    Repetitive_Actions_Initial: float
    Focus_On_Objects_Initial: float
    Social_Interaction_Initial: float
    Outdoor_Change_Initial: float
    Therapy_Engagement_Initial: float
    Eye_Contact_Followup: float
    Follows_Instructions_Followup: float
    Verbal_Improvement_Followup: float
    Repeats_Words_Followup: float
    Routine_Sensitivity_Followup: float
    Repetitive_Actions_Followup: float
    Focus_On_Objects_Followup: float
    Social_Interaction_Followup: float
    Outdoor_Change_Followup: float
    Therapy_Engagement_Followup: float

class PredictionResponse(BaseModel):
    id: int
    user_id: int
    prediction: int
    improvement_percentage: float
    created_at: datetime

    class Config:
        orm_mode = True

class OverallPredictionResponse(BaseModel):
    user_id: int
    overall_prediction: int
    count: int
    overall_improvement_percentage: float
