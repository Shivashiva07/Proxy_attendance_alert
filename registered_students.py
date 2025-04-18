import os
import json
from resemblyzer import VoiceEncoder, preprocess_wav

# Initialize the voice encoder
encoder = VoiceEncoder()

# Create a database to store voice embeddings
voice_db = {}

# 📥 Ask for the number of students
num_students = int(input("Enter the number of students to register: "))

# 🎯 Register each student's voice
for _ in range(num_students):
    student_name = input("Enter the student's name: ")
    audio_file = input(f"Enter the path to {student_name}'s voice file (e.g., 'voices/voice_name.wav'): ")

    if os.path.exists(audio_file):  # Ensure the file exists
        wav = preprocess_wav(audio_file)
        embedding = encoder.embed_utterance(wav)
        voice_db[student_name] = embedding.tolist()
        print(f"✅ {student_name} registered successfully.")
    else:
        print(f"❌ Error: File {audio_file} not found.")

# 💾 Save the voice_db to a JSON file
with open("voice_db.json", "w") as f:
    json.dump(voice_db, f)

print(f"✅ Registered students: {list(voice_db.keys())}")
