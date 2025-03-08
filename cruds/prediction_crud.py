from sqlalchemy.orm import Session
from models.prediction_model import Prediction
from shemas.prediction_shema import PredictionCreate

def create_prediction(db: Session, prediction: PredictionCreate, predicted_label: int, improvement_percentage: float):
    db_prediction = Prediction(
        user_id=prediction.user_id,
        Eye_Contact_Initial=prediction.Eye_Contact_Initial,
        Follows_Instructions_Initial=prediction.Follows_Instructions_Initial,
        Verbal_Improvement_Initial=prediction.Verbal_Improvement_Initial,
        Repeats_Words_Initial=prediction.Repeats_Words_Initial,
        Routine_Sensitivity_Initial=prediction.Routine_Sensitivity_Initial,
        Repetitive_Actions_Initial=prediction.Repetitive_Actions_Initial,
        Focus_On_Objects_Initial=prediction.Focus_On_Objects_Initial,
        Social_Interaction_Initial=prediction.Social_Interaction_Initial,
        Outdoor_Change_Initial=prediction.Outdoor_Change_Initial,
        Therapy_Engagement_Initial=prediction.Therapy_Engagement_Initial,
        Eye_Contact_Followup=prediction.Eye_Contact_Followup,
        Follows_Instructions_Followup=prediction.Follows_Instructions_Followup,
        Verbal_Improvement_Followup=prediction.Verbal_Improvement_Followup,
        Repeats_Words_Followup=prediction.Repeats_Words_Followup,
        Routine_Sensitivity_Followup=prediction.Routine_Sensitivity_Followup,
        Repetitive_Actions_Followup=prediction.Repetitive_Actions_Followup,
        Focus_On_Objects_Followup=prediction.Focus_On_Objects_Followup,
        Social_Interaction_Followup=prediction.Social_Interaction_Followup,
        Outdoor_Change_Followup=prediction.Outdoor_Change_Followup,
        Therapy_Engagement_Followup=prediction.Therapy_Engagement_Followup,
        prediction=predicted_label,
        improvement_percentage=improvement_percentage
    )
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction

def get_predictions_by_user(db: Session, user_id: str):
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()
