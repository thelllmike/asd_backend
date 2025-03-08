from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from db import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    
    # Feature columns
    Eye_Contact_Initial = Column(Float)
    Follows_Instructions_Initial = Column(Float)
    Verbal_Improvement_Initial = Column(Float)
    Repeats_Words_Initial = Column(Float)
    Routine_Sensitivity_Initial = Column(Float)
    Repetitive_Actions_Initial = Column(Float)
    Focus_On_Objects_Initial = Column(Float)
    Social_Interaction_Initial = Column(Float)
    Outdoor_Change_Initial = Column(Float)
    Therapy_Engagement_Initial = Column(Float)
    
    Eye_Contact_Followup = Column(Float)
    Follows_Instructions_Followup = Column(Float)
    Verbal_Improvement_Followup = Column(Float)
    Repeats_Words_Followup = Column(Float)
    Routine_Sensitivity_Followup = Column(Float)
    Repetitive_Actions_Followup = Column(Float)
    Focus_On_Objects_Followup = Column(Float)
    Social_Interaction_Followup = Column(Float)
    Outdoor_Change_Followup = Column(Float)
    Therapy_Engagement_Followup = Column(Float)
    
    # Prediction label and improvement percentage
    prediction = Column(Integer)
    improvement_percentage = Column(Float, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
