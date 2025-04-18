from sounddevice import rec, wait
from scipy.io.wavfile import write

def record_from_mic(filename="voice_test.wav", duration=5, fs=16000):
    print(f"🎙️ Recording for {duration} seconds...")
    audio = rec(int(duration * fs), samplerate=fs, channels=1)
    wait()
    write(filename, fs, audio)
    print(f"✅ Saved recording to {filename}")

record_from_mic()
