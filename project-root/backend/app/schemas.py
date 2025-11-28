"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str

class PredictionRequest(BaseModel):
    """Audio prediction request"""
    audio_file: str
    model_type: str = "mfcc"

class AccentPrediction(BaseModel):
    """Accent prediction result"""
    accent: str
    confidence: float
    language: str

class RecommendationResponse(BaseModel):
    """Restaurant recommendation response"""
    accent: str
    confidence: float
    recommendations: List[str]
    cuisine_suggestions: List[str]

class PredictionResponse(BaseModel):
    """Complete prediction response"""
    prediction: AccentPrediction
    recommendations: Optional[RecommendationResponse] = None
