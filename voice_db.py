import os
import json
from resemblyzer import VoiceEncoder, preprocess_wav

encoder = VoiceEncoder()
voice_db = {}

# List of students and their voice files
students = {
    "shiva": "voice_shiva.wav",
    "mayank": "voice_mayank.wav",
    "balveer": "voice_balveer.wav"
}

# Create voice embeddings
for name, file in students.items():
    if os.path.exists(file):
        wav = preprocess_wav(file)
        embedding = encoder.embed_utterance(wav)
        voice_db[name] = embedding.tolist()
        print(f"✅ Embedded: {name}")
    else:
        print(f"⚠️ File not found: {file}")

# Save embeddings to JSON
with open("voice_db.json", "w") as f:
    json.dump(voice_db, f)

print("\n📦 Saved voice database to voice_db.json")
