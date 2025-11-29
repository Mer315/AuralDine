"""
Utility helpers for audio preprocessing
"""
import io
import tempfile
import numpy as np
import librosa
from pathlib import Path

from app.config import settings


def read_audio_bytes(data: bytes, sr: int = None):
    """
    Read raw audio bytes into a numpy array and return (y, sr)
    Supports WebM, MP3, WAV, and other formats.
    """
    sr = sr or settings.SAMPLE_RATE
    try:
        # Write bytes to temporary file with proper extension
        # This allows librosa to auto-detect format
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        
        try:
            # Load audio from temp file
            y, file_sr = librosa.load(tmp_path, sr=None)
            
            # Resample to target sample rate if needed
            if file_sr != sr:
                y = librosa.resample(y, orig_sr=file_sr, target_sr=sr)
            
            return y, sr
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)
            
    except Exception as e:
        raise RuntimeError(f"Failed to read audio bytes: {e}")


def extract_mfcc(y: np.ndarray, sr: int = None, n_mfcc: int = 13):
    """Extract MFCC features from audio signal."""
    sr = sr or settings.SAMPLE_RATE
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    # Return mean over time axis
    return np.mean(mfcc, axis=1)
