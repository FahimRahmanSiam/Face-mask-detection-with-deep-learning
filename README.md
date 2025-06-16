# 🛡️ Real-Time Face Mask Detection App

A real-time face mask detection app built with **Streamlit**, **OpenCV**, and **TensorFlow** that uses your webcam to detect whether people are wearing masks.

---

## 🧰 Prerequisites

- Python **3.10** (Recommended)
- Git installed
- Internet connection to download packages

---

## 📥 Step 1: Clone the Repository

Open a terminal and run:

```bash
git clone https://github.com/FahimRahmanSiam/Face-mask-detection-with-deep-learning.git
cd Face-mask-detection-with-deep-learning

## 🛠️ Step 2: Create a Virtual Environment
It’s recommended to use a virtual environment to avoid conflicts.

mac/linux:
python3 -m venv facemask-env
source facemask-env/bin/activate

windows:
python -m venv facemask-env
facemask-env\Scripts\activate

## 📦 Step 3: Install Dependencies
pip install -r requirements.txt

## ▶️ Step 4: Run the App
streamlit run app.py
http://localhost:8501


🧠 How It Works
Detects faces in video frames using OpenCV DNN
Classifies each detected face using a MobileNetV2 deep learning model
Real-time feedback on screen using Streamlit + WebRTC
