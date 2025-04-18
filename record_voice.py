# record_voice.py
import pyaudio
import wave

# Settings
FORMAT = pyaudio.paInt16  # 16-bit resolution
CHANNELS = 1              # Mono
RATE = 44100              # 44.1kHz sampling rate
CHUNK = 1024              # 2^10 samples per chunk
RECORD_SECONDS = 5        # Duration of recording
WAVE_OUTPUT_FILENAME = "voice_test.wav"

# Start Recording
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("🎙️ Recording... Speak now!")

frames = []
for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("✅ Recording finished!")

# Stop Recording
stream.stop_stream()
stream.close()
audio.terminate()

# Save file
with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"🎧 Saved to {WAVE_OUTPUT_FILENAME}")
