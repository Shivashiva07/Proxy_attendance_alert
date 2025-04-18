from resemblyzer import preprocess_wav, VoiceEncoder
import numpy as np
import json
import csv
import os
from sounddevice import rec, wait
from scipy.io.wavfile import write
import time

def record_voice(filename, duration=5, fs=16000):
    print(f"\n🎤 Recording voice for next student...")
    audio = rec(int(duration * fs), samplerate=fs, channels=1)
    wait()
    write(filename, fs, audio)
    print(f"✅ Saved {filename}")

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def log_attendance(name, status, filename="attendance_log.csv"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    row = [name, timestamp, status]
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Name", "Timestamp", "Status"])
        writer.writerow(row)
    print(f"📝 Logged: {row}")

def identify_speaker(test_file, encoder, voice_db, threshold=0.80):
    test_wav = preprocess_wav(test_file)
    test_embed = encoder.embed_utterance(test_wav)

    for name, stored_embed in voice_db.items():
        sim = cosine_similarity(test_embed, stored_embed)
        print(f"🔸 Similarity with {name}: {sim:.4f}")
        if sim >= threshold:
            return name, sim
    return None, 0.0

def batch_attendance(num_students, voice_db_path="voice_db.json"):
    encoder = VoiceEncoder()

    with open(voice_db_path, "r") as f:
        voice_db = json.load(f)

    for i in range(num_students):
        filename = f"test_student_{i+1}.wav"
        record_voice(filename)
        name, sim = identify_speaker(filename, encoder, voice_db)

        if name:
            print(f"✅ Attendance marked for {name} (sim={sim:.4f})")
            log_attendance(name, "Present")
        else:
            print("❌ Proxy suspected or unrecognized speaker.")
            log_attendance("Unknown", "Proxy Attempt")

# 🚀 Start batch attendance
batch_attendance(num_students=3)
