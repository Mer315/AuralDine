"""Utility helpers for audio preprocessing

This module implements a full audio preprocessing pipeline used before
inference. It replaces the previous simple MFCC extraction with a
multi-step process including silence trimming, normalization,
pre-emphasis, segmentation, augmentation (jittering), rolling-window
embeddings and fixed-window preparation for models like HuBERT.

The `extract_mfcc` function retains its name/signature but now returns
an aggregated 1D feature vector (mean-pooled MFCC embeddings) so it
remains compatible with the existing `ModelService.predict_from_features`
callsites.
"""

import io
import tempfile
from typing import List, Tuple

import numpy as np
import librosa
from pathlib import Path

from app.config import settings


def read_audio_bytes(data: bytes, sr: int = None) -> Tuple[np.ndarray, int]:
    """Read raw audio bytes into a numpy array and return (y, sr).

    Supports WebM, MP3, WAV and other formats by writing the bytes to a
    temporary file and letting librosa detect the format.
    """
    sr = sr or settings.SAMPLE_RATE
    try:
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name

        try:
            y, file_sr = librosa.load(tmp_path, sr=None)
            if file_sr != sr:
                y = librosa.resample(y, orig_sr=file_sr, target_sr=sr)
            return y, sr
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    except Exception as e:
        raise RuntimeError(f"Failed to read audio bytes: {e}")


# ----------------------------- Helper steps -----------------------------
def trim_silence(y: np.ndarray, top_db: int = 20) -> np.ndarray:
    """Trim leading and trailing silence from audio using librosa.effects.trim."""
    try:
        y_trim, _ = librosa.effects.trim(y, top_db=top_db)
        return y_trim
    except Exception:
        # If trimming fails, return original
        return y


def normalize_audio(y: np.ndarray) -> np.ndarray:
    """Normalize audio by peak amplitude (avoid division by zero)."""
    peak = np.max(np.abs(y))
    if peak <= 0:
        return y
    return y / (peak + 1e-9)


def pre_emphasize(y: np.ndarray, coef: float = 0.97) -> np.ndarray:
    """Apply a pre-emphasis filter y[t] = y[t] - coef * y[t-1]."""
    if y.size == 0:
        return y
    y_emph = np.append(y[0], y[1:] - coef * y[:-1])
    return y_emph


def split_segments(y: np.ndarray, sr: int, seg_length_sec: float = 1.5) -> List[np.ndarray]:
    """Split audio into fixed-length raw segments (pad last segment with zeros).

    Returns a list of numpy arrays each of length seg_length_sec*sr.
    """
    seg_samples = int(seg_length_sec * sr)
    if seg_samples <= 0:
        return []

    total_samples = len(y)
    segments = []
    for start in range(0, total_samples, seg_samples):
        seg = y[start:start + seg_samples]
        if len(seg) < seg_samples:
            seg = librosa.util.fix_length(data=seg, size=seg_samples)

        segments.append(seg)

    # If audio shorter than one segment, ensure we have at least one padded segment
    if len(segments) == 0:
        segments = [librosa.util.fix_length(y, size=seg_samples)]

    return segments


def apply_jitter(y: np.ndarray, sr: int) -> List[np.ndarray]:
    """Return a list containing the original waveform plus a few jittered variants.

    Jittering options (one randomly applied per augmented copy):
      - speed change (0.9 - 1.1)
      - pitch shift (-1 to +1 semitone)
      - small additive Gaussian noise

    The original waveform is always included first.
    """
    variants = [y]

    # Speed change variant
    try:
        rate = float(np.random.uniform(0.9, 1.1))
        y_stretch = librosa.effects.time_stretch(y, rate)
        # Resample or trim/pad back to original length
        y_stretch = librosa.util.fix_length(y_stretch, size=len(y))
        variants.append(y_stretch)
    except Exception:
        pass

    # Pitch shift variant
    try:
        n_steps = float(np.random.uniform(-1.0, 1.0))
        y_pitch = librosa.effects.pitch_shift(y, sr, n_steps=n_steps)
        y_pitch = librosa.util.fix_length(y_pitch, size=len(y))
        variants.append(y_pitch)
    except Exception:
        pass

    # Additive noise variant
    try:
        noise_amp = 1e-4 * np.max(np.abs(y)) if np.max(np.abs(y)) > 0 else 1e-4
        y_noise = y + np.random.normal(0, noise_amp, size=y.shape)
        variants.append(y_noise)
    except Exception:
        pass

    # Ensure uniqueness and limit count
    unique_variants = []
    for v in variants:
        if not any(np.array_equal(v, u) for u in unique_variants):
            unique_variants.append(v)

    return unique_variants


def rolling_windows(y: np.ndarray, sr: int, window_sec: float = 1.0, hop_sec: float = 0.5,
                    n_mfcc: int = 13) -> np.ndarray:
    """Compute per-window embeddings (MFCC mean) across rolling windows.

    Returns a 2D array of shape (num_windows, n_mfcc). Caller can aggregate.
    """
    win_samples = int(window_sec * sr)
    hop_samples = int(hop_sec * sr)
    if win_samples <= 0:
        return np.zeros((0, n_mfcc))

    windows = []
    for start in range(0, max(1, len(y) - win_samples + 1), hop_samples):
        w = y[start:start + win_samples]
        if len(w) < win_samples:
            w = librosa.util.fix_length(w, size=win_samples)
        mfcc = librosa.feature.mfcc(y=w, sr=sr, n_mfcc=n_mfcc)
        mfcc_mean = np.mean(mfcc, axis=1)
        windows.append(mfcc_mean)

    if len(windows) == 0:
        # Fallback: compute for a single padded window
        w = librosa.util.fix_length(y, size=win_samples)
        mfcc = librosa.feature.mfcc(y=w, sr=sr, n_mfcc=n_mfcc)
        return np.mean(mfcc, axis=1)[np.newaxis, :]

    return np.stack(windows, axis=0)


def prepare_fixed_windows(y: np.ndarray, sr: int, window_sec: float = 1.0) -> List[np.ndarray]:
    """Produce a list of fixed-length windows (pad or crop) for inference.

    Useful for models (like HuBERT) that require uniform-length inputs.
    Each returned window has length int(window_sec * sr).
    """
    win_samples = int(window_sec * sr)
    windows = []
    # Slide with non-overlapping windows across the segment
    for start in range(0, len(y), win_samples):
        w = y[start:start + win_samples]
        if len(w) < win_samples:
            w = librosa.util.fix_length(w, size=win_samples)
        windows.append(w)
    if len(windows) == 0:
        windows = [librosa.util.fix_length(y, size=win_samples)]
    return windows


# ------------------------- High-level pipeline API -----------------------
def extract_mfcc(y: np.ndarray, sr: int = None, n_mfcc: int = 13, fast: bool = False) -> np.ndarray:
    """Full preprocessing + embedding extraction.

    Steps implemented (in order):
      1. Silence trimming (librosa.effects.trim top_db=20)
      2. Normalization (peak)
      3. Pre-emphasis (coef=0.97)
      4. Segment splitting (1.5s segments, pad if needed)
      5. Jittering: keep original + augmented variants
      6. Rolling embeddings: overlapping windows per segment (1s window, 0.5s hop)
      7. Fixed-window segmentation helper for model inputs (1s windows)

    The function returns a single 1D numpy array compatible with
    `ModelService.predict_from_features` (shape: (n_mfcc,)).
    """
    sr = sr or settings.SAMPLE_RATE

    # Fast mode: simpler, fewer augmentations and windows to reduce CPU time
    if fast:
        # 1. Trim silence, normalize, pre-emphasis
        y_proc = trim_silence(y, top_db=20)
        y_proc = normalize_audio(y_proc)
        y_proc = pre_emphasize(y_proc, coef=0.97)

        # Use single 1s non-overlapping windows (fewer MFCC calls)
        segments = split_segments(y_proc, sr, seg_length_sec=1.0)
        window_embs = []
        for seg in segments:
            try:
                mf = librosa.feature.mfcc(y=seg, sr=sr, n_mfcc=n_mfcc)
                window_embs.append(np.mean(mf, axis=1))
            except Exception:
                window_embs.append(np.zeros(n_mfcc))

        if len(window_embs) == 0:
            mf = librosa.feature.mfcc(y=y_proc, sr=sr, n_mfcc=n_mfcc)
            return np.mean(mf, axis=1)

        return np.mean(np.stack(window_embs, axis=0), axis=0)

    # Original (slower, higher-accuracy) pipeline
    sr = sr or settings.SAMPLE_RATE

    # 1. Silence trimming
    y_proc = trim_silence(y, top_db=20)

    # 2. Normalization
    y_proc = normalize_audio(y_proc)

    # 3. Pre-emphasis
    y_proc = pre_emphasize(y_proc, coef=0.97)

    # 4. Segment splitting (1.5s)
    segments = split_segments(y_proc, sr, seg_length_sec=1.5)

    segment_embeddings = []
    for seg in segments:
        # 5. Jittering -> produce list of variants (original + aug)
        variants = apply_jitter(seg, sr)

        variant_embeddings = []
        for v in variants:
            # 6. Rolling embeddings: 1s windows with 0.5s hop
            win_embs = rolling_windows(v, sr, window_sec=1.0, hop_sec=0.5, n_mfcc=n_mfcc)
            # Aggregate per-variant by mean pooling over windows
            if win_embs.size == 0:
                continue
            pooled = np.mean(win_embs, axis=0)
            variant_embeddings.append(pooled)

        # If no variant embeddings were produced, fallback to MFCC of the seg
        if len(variant_embeddings) == 0:
            mf = librosa.feature.mfcc(y=seg, sr=sr, n_mfcc=n_mfcc)
            segment_embeddings.append(np.mean(mf, axis=1))
            continue

        # Aggregate across variants for this segment (mean)
        segment_emb = np.mean(np.stack(variant_embeddings, axis=0), axis=0)
        segment_embeddings.append(segment_emb)

    # Aggregate across segments to a single feature vector (mean pooling)
    if len(segment_embeddings) == 0:
        # As a last fallback compute MFCC on whole signal
        mf = librosa.feature.mfcc(y=y_proc, sr=sr, n_mfcc=n_mfcc)
        return np.mean(mf, axis=1)

    final_embedding = np.mean(np.stack(segment_embeddings, axis=0), axis=0)

    # final_embedding is shape (n_mfcc,) - compatible with existing predict API
    return final_embedding


def prepare_model_windows_from_audio(y: np.ndarray, sr: int, window_sec: float = 1.0) -> List[np.ndarray]:
    """Convenience function: run trimming/normalize/preemph and produce
    fixed windows ready for a frame-wise model (e.g., HuBERT).

    Returns list of 1-sec windows (numpy arrays) each exactly length sr*window_sec.
    """
    y_proc = trim_silence(y, top_db=20)
    y_proc = normalize_audio(y_proc)
    y_proc = pre_emphasize(y_proc, coef=0.97)

    # Split into longer segments first to keep consistent behavior
    segments = split_segments(y_proc, sr, seg_length_sec=1.5)
    windows = []
    for seg in segments:
        seg_windows = prepare_fixed_windows(seg, sr, window_sec=window_sec)
        windows.extend(seg_windows)
    return windows


def preprocess_audio(y: np.ndarray, sr: int, window_sec: float = 1.0, n_mfcc: int = 13, fast: bool = False):
    """Run the full preprocessing pipeline and return a dictionary with
    processed windows and summary statistics useful for debugging/UI.

    Returns a dict with keys:
      - 'sr', 'original_samples', 'num_segments', 'num_windows'
      - 'mfcc_means': list of per-window mean MFCC vectors (as lists)
      - 'windows': list of numpy arrays (the fixed-length windows)
    """
    # Fast preprocessing: fewer windows and skip augmentations
    if fast:
        y_proc = trim_silence(y, top_db=20)
        y_proc = normalize_audio(y_proc)
        y_proc = pre_emphasize(y_proc, coef=0.97)

        segments = split_segments(y_proc, sr, seg_length_sec=1.0)
        windows = []
        for seg in segments:
            seg_windows = prepare_fixed_windows(seg, sr, window_sec=window_sec)
            windows.extend(seg_windows)

        mfcc_means = []
        for w in windows:
            try:
                mf = librosa.feature.mfcc(y=w, sr=sr, n_mfcc=n_mfcc)
                mfcc_means.append(np.mean(mf, axis=1).tolist())
            except Exception:
                mfcc_means.append([0.0] * n_mfcc)

        return {
            'sr': int(sr),
            'original_samples': int(len(y)),
            'num_segments': int(len(segments)),
            'num_windows': int(len(windows)),
            'mfcc_means': mfcc_means,
            'windows': windows,
        }

    # Original full pipeline
    # Trim/normalize/pre-emphasis
    y_proc = trim_silence(y, top_db=20)
    y_proc = normalize_audio(y_proc)
    y_proc = pre_emphasize(y_proc, coef=0.97)

    # Split into segments then fixed windows
    segments = split_segments(y_proc, sr, seg_length_sec=1.5)
    windows = []
    for seg in segments:
        seg_windows = prepare_fixed_windows(seg, sr, window_sec=window_sec)
        windows.extend(seg_windows)

    # Compute per-window MFCC mean embeddings
    mfcc_means = []
    for w in windows:
        try:
            mf = librosa.feature.mfcc(y=w, sr=sr, n_mfcc=n_mfcc)
            mf_mean = np.mean(mf, axis=1)
            mfcc_means.append(mf_mean.tolist())
        except Exception:
            # if MFCC fails, append zeros
            mfcc_means.append([0.0] * n_mfcc)

    return {
        'sr': int(sr),
        'original_samples': int(len(y)),
        'num_segments': int(len(segments)),
        'num_windows': int(len(windows)),
        'mfcc_means': mfcc_means,
        'windows': windows,
    }
