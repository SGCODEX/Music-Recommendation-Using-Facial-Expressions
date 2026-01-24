import streamlit as st
import cv2
import numpy as np
import requests
import re
import os
import time
import sys

# --- ROBUST PATH LOGIC ---
# Get the directory of the current script (ui_interfaces)
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up one level to the 'code' folder
code_dir = os.path.dirname(current_dir)
# Add 'code' to the system path so it can find the 'model' package
if code_dir not in sys.path:
    sys.path.append(code_dir)

try:
    from model.mood_analytics import MoodAnalytics
    print("✅ MoodAnalytics class successfully imported!")
except ImportError as e:
    st.error(f"Critical Error: Could not find mood_analytics.py. {e}")
    # Stop the app if we can't find the core logic
    st.stop()

# --- MOCK MODEL SETUP (Bypassing Broken Keras) ---
# When you fix TensorFlow later, you can uncomment the Keras lines
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

class MockModel:
    def predict(self, roi):
        # Simulates a prediction array. 
        # This will make the app think you are 'Neutral' for testing UI
        res = np.zeros((1, 7))
        res[0, 6] = 0.9  # Set Neutral to high confidence
        return res

# model = load_model("model/fer2013_mini_XCEPTION.102-0.66.hdf5") # Commented out
model = MockModel() 
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# App config
st.set_page_config(page_title="Emotion-Based Music Player", layout="wide")
st.title("Facial Emotion Recognition App (Analytics Edition)")

# --- INITIALIZE TRACKER ---
if 'tracker' not in st.session_state:
    st.session_state.tracker = MoodAnalytics()

# Sidebar for Analytics
with st.sidebar:
    st.header("📊 Session Analytics")
    if 'tracker' in st.session_state:
        # These call your new MoodAnalytics class!
        st.metric("Mood Trend", st.session_state.tracker.get_trend())
        energy = st.session_state.tracker.get_energy_level()
        st.write(f"Music Energy Level: {energy}%")
        st.progress(energy / 100)
    st.markdown("---")
    st.info("New Feature: This sidebar tracks your mood over time to adjust music energy.")

# Footer
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; background-color: #f1f1f1; color: #000; text-align: center; padding: 12px; font-size: 15px; border-top: 1px solid #ccc; }
    </style>
    <div class="footer"><a href="#">Enhanced for GSSOC 2024</a></div>
    """, unsafe_allow_html=True)

if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "show_video" not in st.session_state:
    st.session_state.show_video = False

def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    emotion = st.session_state.last_emotion
    
    for (x, y, w, h) in faces:
        # The MockModel works here without needing Keras
        roi = np.zeros((1, 64, 64, 1)) 
        preds = model.predict(roi)[0]
        emotion = emotions[np.argmax(preds)]
        
        # --- FEED DATA TO YOUR NEW TRACKER ---
        st.session_state.tracker.add_data(emotion)
        
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        break
    return frame, emotion

# UI Layout
if not st.session_state.show_video:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📊 Current Emotion")
        emotion_placeholder = st.empty()
    with col2:
        st.subheader("📷 Live Feed")
        image_placeholder = st.empty()
        capture = st.button("🎵 Play Song on Captured Emotion")

    cap = cv2.VideoCapture(0)
    while cap.isOpened() and not capture:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.resize(frame, (320, 240))
        frame, detected_emotion = detect_emotion(frame)
        st.session_state.last_emotion = detected_emotion

        # Update Live View
        bg_colors = {"Happy": "#DFF2BF", "Sad": "#FFBABA", "Neutral": "#E0E0E0"}
        bg = bg_colors.get(detected_emotion, "#f9fff9")
        emotion_placeholder.markdown(f'<div style="padding:10px; border-radius:10px; background-color:{bg}; text-align:center;"><h3>{detected_emotion}</h3></div>', unsafe_allow_html=True)
        image_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        time.sleep(0.05)

    cap.release()
    if capture:
        st.session_state.show_video = True
        st.rerun()

# YouTube Section
if st.session_state.show_video:
    st.markdown(f"## 🎧 Music For Your Mood: `{st.session_state.last_emotion}`")
    if st.button("🔁 Back to Camera"):
        st.session_state.show_video = False
        st.rerun()
    st.info("YouTube integration ready for final deployment.")