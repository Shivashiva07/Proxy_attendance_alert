from resemblyzer import preprocess_wav, VoiceEncoder
import numpy as np
import json
import csv
import os
from sounddevice import rec, wait
from scipy.io.wavfile import write
import time

def record_test_voice(filename="test_voice.wav", duration=5, fs=16000):
    print("🎤 Recording attendance voice...")
    audio = rec(int(duration * fs), samplerate=fs, channels=1)
    wait()
    write(filename, fs, audio)
    print(f"✅ Saved test voice to {filename}")

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

def check_attendance(voice_db_path="voice_db.json", threshold=0.80):
    record_test_voice()

    encoder = VoiceEncoder()
    test_wav = preprocess_wav("test_voice.wav")
    test_embed = encoder.embed_utterance(test_wav)

    with open(voice_db_path, "r") as f:
        db = json.load(f)

    print("\n🔎 Matching voice with registered students...")
    matched = False
    for name, stored_embed in db.items():
        sim = cosine_similarity(test_embed, stored_embed)
        print(f"🔸 Similarity with {name}: {sim:.4f}")
        if sim >= threshold:
            matched = True
            print(f"\n✅ Attendance marked for {name}")
            log_attendance(name, "Present")
            break

    if not matched:
        print("\n❌ Proxy attempt suspected!")
        log_attendance("Unknown", "Proxy Attempt")

# Run the attendance checker
check_attendance()
