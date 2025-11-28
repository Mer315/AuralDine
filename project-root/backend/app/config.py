"""
Configuration settings for AuralDine backend
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "AuralDine API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Model Settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "ml/models/cnn_bn_final.pt")
    DATASET_PATH: str = os.getenv("DATASET_PATH", "ml/data/label_mfcc_dataset.csv")
    
    # Audio Processing
    SAMPLE_RATE: int = 16000
    N_MFCC: int = 13
    
    class Config:
        env_file = ".env"

settings = Settings()
