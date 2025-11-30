import os
from pathlib import Path

class Settings:
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'native-language-id')
    # Model path - works both locally and in Docker
    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    MODEL_PATH = os.getenv('MODEL_PATH', str(BASE_DIR / 'ml' / 'saved_models' / 'cnn_bn_final.pt'))
    SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', 16000))
    # Enable faster, lower-cost preprocessing by default (set FAST_PREPROCESS=0 to disable)
    FAST_PREPROCESS = bool(int(os.getenv('FAST_PREPROCESS', '1')))

settings = Settings()
