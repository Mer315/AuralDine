"""
Utility helpers for audio preprocessing
"""
import io
import numpy as np
import soundfile as sf
import librosa

from app.config import settings


def read_audio_bytes(data: bytes, sr: int = None):
    """
    Read raw audio bytes into a numpy array and return (y, sr)
    """
    sr = sr or settings.SAMPLE_RATE
    try:
        # Use librosa to load audio from bytes (supports WebM, MP3, WAV, etc.)
        y, file_sr = librosa.load(io.BytesIO(data), sr=None)
        # Resample to target sample rate if needed
        if file_sr != sr:
            y = librosa.resample(y, orig_sr=file_sr, target_sr=sr)
        return y, sr
    except Exception as e:
        raise RuntimeError(f"Failed to read audio bytes: {e}")


def extract_mfcc(y: np.ndarray, sr: int = None, n_mfcc: int = 13):
    sr = sr or settings.SAMPLE_RATE
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    # Return mean over time axis
    return np.mean(mfcc, axis=1)
