import time
import wave
import struct
import math
from pathlib import Path

# generate a 1s 16kHz sine wave and save as test.wav
sr = 16000
dur = 1.0
freq = 220.0
samples = int(sr * dur)
path = Path(__file__).parent / 'test.wav'
with wave.open(str(path), 'w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    for i in range(samples):
        t = i / sr
        val = int(32767 * 0.5 * math.sin(2 * math.pi * freq * t))
        wf.writeframes(struct.pack('<h', val))

print('WAV created at', path)

# Now import preprocessing functions
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.utils import read_audio_bytes, extract_mfcc, prepare_model_windows_from_audio

# Read bytes
with open(path, 'rb') as f:
    data = f.read()

print('Read bytes length:', len(data))

start = time.time()
y, sr = read_audio_bytes(data)
print('read_audio_bytes -> y.shape, sr:', y.shape, sr, 'took', time.time()-start)

start = time.time()
feat = extract_mfcc(y, sr=sr, n_mfcc=13)
print('extract_mfcc -> feat.shape:', feat.shape if hasattr(feat, 'shape') else type(feat), 'took', time.time()-start)
print('feat (first 5):', feat[:5])

start = time.time()
windows = prepare_model_windows_from_audio(y, sr, window_sec=1.0)
print('prepare_model_windows_from_audio -> windows:', len(windows), 'each len', [len(w) for w in windows], 'took', time.time()-start)
