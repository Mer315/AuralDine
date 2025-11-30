import wave, math, struct
sr=16000
duration=1.0
freq=440.0
n=int(sr*duration)
with wave.open('test_tone.wav','w') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(sr)
    for i in range(n):
        val = int(32767.0*0.5*math.sin(2*math.pi*freq*i/sr))
        wf.writeframes(struct.pack('<h', val))
print('WAV created: test_tone.wav')
