"""
Prediction endpoint for accent recognition
"""
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.schemas import PredictionResponse, AccentPrediction
from app.services.mfcc_predictor import MFCCPredictor
from app.services.recommender import Recommender

router = APIRouter()
predictor = MFCCPredictor()
recommender = Recommender()

@router.post("/predict", response_model=PredictionResponse)
async def predict_accent(file: UploadFile = File(...)):
    """
    Predict accent from audio file
    """
    try:
        # Read audio file
        content = await file.read()
        
        # Make prediction
        prediction = predictor.predict(content)
        
        # Get recommendations
        recommendations = recommender.get_recommendations(prediction["accent"])
        
        return {
            "prediction": {
                "accent": prediction["accent"],
                "confidence": prediction["confidence"],
                "language": prediction.get("language", "Unknown")
            },
            "recommendations": recommendations
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
