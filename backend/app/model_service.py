"""
Model service: load model and make predictions
"""
import os
import torch
import numpy as np
from app.config import settings

# Mapping indices to states (example mapping)
STATE_MAPPING = [
    'andhrapradesh', 'gujarath', 'kerala', 'karnataka', 'jharkhand', 'tamilnadu'
]

class ModelService:
    def __init__(self, model_path: str = None):
        self.model_path = model_path or settings.MODEL_PATH
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None

    def load_model(self):
        if self.model is not None:
            return self.model
        
        print(f"Loading model from: {self.model_path}")
        
        if not os.path.exists(self.model_path):
            print(f"Warning: Model file not found at {self.model_path}")
            print("Using deterministic dummy predictions instead")
            self.model = None
            return None
        try:
            self.model = torch.load(self.model_path, map_location=self.device)
            self.model.eval()
            print("Model loaded successfully")
            return self.model
        except Exception as e:
            print(f"Warning: failed to load model: {e}")
            self.model = None
            return None

    def predict_from_features(self, features: np.ndarray):
        """Predict state index from feature vector. Returns (state, confidence)."""
        # If model is not available, return deterministic dummy prediction
        if self.model is None:
            # Simple heuristic: sum features to pick index
            idx = int(abs(int(np.sum(features))) % len(STATE_MAPPING))
            return STATE_MAPPING[idx], 0.5

        try:
            # Convert features to tensor
            import torch
            with torch.no_grad():
                x = torch.from_numpy(features).float().unsqueeze(0).to(self.device)
                out = self.model(x)
                if isinstance(out, (list, tuple)):
                    out = out[0]
                probs = torch.softmax(out, dim=-1).cpu().numpy()[0]
                idx = int(np.argmax(probs))
                conf = float(probs[idx])
                state = STATE_MAPPING[idx] if idx < len(STATE_MAPPING) else 'unknown'
                return state, conf
        except Exception as e:
            print(f"Prediction failed: {e}")
            return 'unknown', 0.0
