"""
Model loading utilities
"""
import torch
from pathlib import Path
from app.config import settings

class ModelLoader:
    """Load and manage ML models"""
    
    def __init__(self):
        """Initialize model loader"""
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    def load_model(self, model_path: str = None):
        """
        Load PyTorch model
        
        Args:
            model_path: Path to model file
        """
        path = model_path or settings.MODEL_PATH
        if not Path(path).exists():
            raise FileNotFoundError(f"Model not found at {path}")
        
        self.model = torch.load(path, map_location=self.device)
        self.model.eval()
        return self.model
    
    def get_model(self):
        """Get loaded model"""
        if self.model is None:
            self.load_model()
        return self.model
