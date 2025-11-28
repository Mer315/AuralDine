import os

class Settings:
    PROJECT_NAME = os.getenv('PROJECT_NAME', 'native-language-id')
    MODEL_PATH = os.getenv('MODEL_PATH', '../../ml/saved_models/cnn_bn_final.pt')
    SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', 16000))

settings = Settings()
