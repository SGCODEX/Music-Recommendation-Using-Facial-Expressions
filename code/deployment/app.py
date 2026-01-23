from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import webbrowser
import requests
import re
import os
import time

# Load model and labels
model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5")
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# App config
st.set_page_config(page_title="Emotion-Based Music Player", layout="centered")
st.title("Facial Emotion Recognition App")
st.write("This app detects your facial expression and plays a suitable song.")

# Footer
st.markdown(
    """
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background: linear-gradient(135deg, rgba(223, 242, 191, 0.9) 0%, rgba(176, 255, 186, 0.9) 50%, rgba(255, 255, 186, 0.9) 100%);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    color: #2c3e50;
    text-align: center;
    padding: 15px 0;
    font-size: 14px;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
    z-index: 9999;
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    border-top: 1px solid rgba(255,255,255,0.4);
    transition: all 0.3s ease;
}

.footer-content {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    gap: 8px;
}

.footer a {
    color: #1b5e20;
    text-decoration: none;
    font-weight: 700;
    position: relative;
    padding: 0 4px;
    transition: all 0.3s ease;
}

.footer a:hover {
    color: #0d3b10;
    text-shadow: 0 0 10px rgba(27, 94, 32, 0.2);
    transform: translateY(-1px);
}

.footer a::after {
    content: '';
    position: absolute;
    width: 0;
    height: 2px;
    bottom: -2px;
    left: 50%;
    background-color: #1b5e20;
    transition: all 0.3s ease;
    transform: translateX(-50%);
}

.footer a:hover::after {
    width: 100%;
}

.footer-emoji {
    display: inline-block;
    font-size: 1.2em;
    margin: 0 5px;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}

.badge-container {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 4px;
}

.footer-badge {
    background: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.8);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.85em;
    font-weight: 600;
    color: #444;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
    cursor: default;
}

.footer-badge:hover {
    background: rgba(255, 255, 255, 0.9);
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    color: #1b5e20;
}
</style>

<div class="footer">
    <div class="footer-content">
        <div>
            <span class="footer-emoji">🎵</span>
            Designed & Developed by 
            <a href="https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git" target="_blank">
                SGCODEX
            </a>
            <span class="footer-emoji">⭐</span>
        </div>
        
        <div class="badge-container">
            <span style="font-size: 0.9em; align-self: center; margin-right: 5px;">Proudly part of:</span>
            <span class="footer-badge" title="Semester Long Open Source Program">SWOC</span>
            <span class="footer-badge" title="IEEE Indira Gandhi Delhi Technical University for Women">IEEE-IGDTUW</span>
            <span class="footer-badge" title="GirlScript Summer of Code">GSSOC</span>
        </div>
    </div>
</div>
    """,
    unsafe_allow_html=True
)

# App state
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "show_video" not in st.session_state:
    st.session_state.show_video = False

# Streamlit WebRTC Video Transformer
class EmotionDetector(VideoTransformerBase):
    def __init__(self):
        self.last_emotion = "Neutral"

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (64, 64))
            roi = roi_gray.astype("float") / 255.0
            roi = np.expand_dims(roi, axis=0)
            roi = np.expand_dims(roi, axis=-1)
            preds = model.predict(roi)[0]
            self.last_emotion = emotions[np.argmax(preds)]
            st.session_state.last_emotion = self.last_emotion

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, self.last_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            break

        return img

# 🎥 Live Camera Detection Mode
if not st.session_state.show_video:
    st.subheader("📷 Capturing Your Live Emotions")
    col1, col2 = st.columns([1, 2])  # Adjust the ratio as you prefer

    with col1:
        capture = st.button("🎵 Play Song on Last Captured Emotion")

    with col2:
        # ctx = webrtc_streamer(key="emotion", video_transformer_factory=EmotionDetector)
        # Google's STUN server helps WebRTC webcam work reliably across networks and firewalls.
        # Using public STUN server to establish webcam stream across NAT/firewalls.

        ctx = webrtc_streamer(
            key="emotion",
            video_transformer_factory=EmotionDetector,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            )


    if capture:
        if ctx.video_transformer:
            st.session_state.last_emotion = ctx.video_transformer.last_emotion
            st.session_state.show_video = True
            st.rerun()

# 🎧 Play Song For Detected Mood
if st.session_state.show_video:
    st.markdown("## 🎧 Now Playing Music For Your Mood")
    st.markdown(f"**Last Detected Mood:** `{st.session_state.last_emotion}`")

    if st.button("🔁 Detect Emotions Again"):
        st.session_state.show_video = False
        st.rerun()

    search_query = f"https://www.youtube.com/results?search_query={st.session_state.last_emotion}+background+tunes"
    response = requests.get(search_query)

    if response.status_code != 200:
        print("Failed to retrieve YouTube search results. Status code:", response.status_code)

    html_content = response.text
    match = re.search(r'/watch\?v=([^\"]+)', html_content)
    if match:
        video_id = match.group(1)
        video_url = f"https://www.youtube.com/watch?v={video_id.encode('utf-8').decode('unicode_escape')}"
        st.video(video_url)
        print("Opening YouTube video:", video_url)
