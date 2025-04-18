import os
import json
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from resemblyzer import preprocess_wav, VoiceEncoder
from datetime import datetime

# 🎙️ Function to record from mic
def record_from_mic(filename="voice_test.wav", duration=5, fs=16000):
    print(f"\n🎙️ Recording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print(f"✅ Saved to {filename}")

# 📖 Load saved voice embeddings
def load_voice_db(path="voice_db.json"):
    if not os.path.exists(path):
        print("❌ Voice database not found!")
        return None
    with open(path, "r") as f:
        return json.load(f)

# 📏 Compare two voice embeddings
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

# 📝 Optional: Save attendance log
def save_attendance(student_name, similarity, status, log_file="attendance_log.txt"):
    with open(log_file, "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{now} | {student_name} | Score: {similarity:.4f} | {status}\n")

# 🚀 Main attendance function
def verify_attendance():
    encoder = VoiceEncoder()
    voice_db = load_voice_db()
    if not voice_db:
        return

    student_name = input("\n🧑 Enter your name: ").strip().lower()
    if student_name not in voice_db:
        print(f"❌ Student '{student_name}' not found in the database.")
        return

    # Step 1: Record voice
    record_from_mic()

    # Step 2: Process and compare
    test_wav = preprocess_wav("voice_test.wav")
    test_embed = encoder.embed_utterance(test_wav)

    stored_embed = voice_db[student_name]
    similarity = cosine_similarity(test_embed, stored_embed)

    print(f"\n🔍 Similarity with {student_name}: {similarity:.4f}")

    if similarity > 0.90:
        print("✅ Voice matched. Attendance marked.")
        save_attendance(student_name, similarity, "Present")
    else:
        print("🚨 Proxy detected! Voice doesn't match.")
        save_attendance(student_name, similarity, "Proxy Attempt")

# 🏁 Run it
verify_attendance()
