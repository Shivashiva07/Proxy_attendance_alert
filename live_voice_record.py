import os
import json
from resemblyzer import VoiceEncoder, preprocess_wav
from sounddevice import rec, wait
from scipy.io.wavfile import write

encoder = VoiceEncoder()
voice_db = {}

# 📥 List of students to register
students = ["shiva", "mayank", "balveer"]

# 🎙️ Record and save each student's voice
fs = 16000  # Sample rate
for name in students:
    print(f"\n🎤 Recording for {name}...")
    audio = rec(int(5 * fs), samplerate=fs, channels=1)
    wait()
    filename = f"voice_{name}.wav"
    write(filename, fs, audio)
    print(f"✅ Saved {filename}")

# 🎯 Create embeddings and store them
for name in students:
    file = f"voice_{name}.wav"
    if os.path.exists(file):
        wav = preprocess_wav(file)
        embedding = encoder.embed_utterance(wav)
        voice_db[name] = embedding.tolist()
        print(f"✅ Embedded {name}")
    else:
        print(f"⚠️ Missing file: {file}")

# 💾 Save the database to a JSON file
with open("voice_db.json", "w") as f:
    json.dump(voice_db, f)

print("\n📦 Voice database saved to voice_db.json")
