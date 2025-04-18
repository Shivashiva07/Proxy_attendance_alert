# compare_voices.py
from resemblyzer import VoiceEncoder, preprocess_wav
import numpy as np

# Load audio files
wav1 = preprocess_wav("voice1.wav")
wav2 = preprocess_wav("voice2.wav")

# Load encoder
encoder = VoiceEncoder()

# Get voice embeddings
embed1 = encoder.embed_utterance(wav1)
embed2 = encoder.embed_utterance(wav2)

# Cosine similarity
similarity = np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))

print(f"🔍 Cosine Similarity: {similarity:.4f}")

# Simple decision logic
if similarity > 0.75:
    print("✅ Likely same speaker")
else:
    print("🚨 Proxy detected! Different voices")
