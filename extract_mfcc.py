# extract_mfcc.py
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load the audio file
file_path = "voice_balveer.wav"
y, sr = librosa.load(file_path)

# Extract MFCCs
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

# Plot MFCCs
plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, x_axis='time')
plt.colorbar()
plt.title('MFCC of Recorded Audio')
plt.tight_layout()
plt.show()
