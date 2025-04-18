# 🎤 Proxy Voice Attendance Checker

A voice-based attendance system that detects proxy attendance using voice recognition and alerts the admin of suspicious attempts.

## 🔧 Features
- Record and register student voices
- Match voice samples during attendance marking
- Detect proxy attempts using voice embeddings
- View attendance logs in a dashboard
- (Optional) Get SMS alerts on proxy detection

## 🛠 Tech Stack
- Python
- Resemblyzer (Voice Embeddings)
- Streamlit (Dashboard)
- Twilio (SMS Notifications)

## 🚀 How to Run
```bash
pip install -r requirements.txt
python register_students.py
python attendance_checker.py
streamlit run dashboard.py
```

## 📁 Project Structure
See the folder layout in the repo for scripts, voice samples, and logs.
