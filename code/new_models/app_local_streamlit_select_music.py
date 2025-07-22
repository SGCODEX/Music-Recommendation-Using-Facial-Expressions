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
from urllib.parse import quote_plus

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
        background-color: #f1f1f1;
        color: #000000;
        text-align: center;
        padding: 12px;
        font-size: 15px;
        box-shadow: 0 -1px 4px rgba(0,0,0,0.1);
        border-top: 1px solid #ccc;
        margin-top: 50px;
        z-index: 9999;
    }
    </style>

    <div class="footer">
        <a href="https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git" style="color: #0072E3; text-decoration: underline;">
        Project by SGCODEX. Visit us and give this project a ⭐. Proudly part of open source programs like SWOC, IEEE-IGDTUW, GSSOC and more!!
        </a>
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
    col1, col2 = st.columns([1, 2])

    with col1:
        capture = st.button("🎵 Play Song on Last Captured Emotion")

    with col2:
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
    st.markdown(f"## 🎧 Choose a {st.session_state.last_emotion} song to play")
    st.markdown(f"**Last Detected Mood:** `{st.session_state.last_emotion}`")

    if st.button("🔁 Detect Emotions Again"):
        st.session_state.show_video = False
        st.rerun()

    search_query = f"https://www.youtube.com/results?search_query={quote_plus(st.session_state.last_emotion + ' background tunes')}"
    response = requests.get(search_query)

    if response.status_code != 200:
        st.error("Failed to retrieve YouTube search results.")
    else:
        html_content = response.text
        video_ids = re.findall(r'/watch\?v=([^"]{11})', html_content)
        unique_ids = list(dict.fromkeys(video_ids))[:5]  # Top 5 unique videos

        if unique_ids:
            cols = st.columns(len(unique_ids))
            for i, video_id in enumerate(unique_ids):
                with cols[i]:
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
                    st.image(thumbnail_url, use_container_width=True)
                    if st.button(f"▶️ Play {i+1}", key=video_id):
                        st.session_state.selected_video = video_url

            if "selected_video" in st.session_state:
                st.video(st.session_state.selected_video)
        else:
             st.warning("No music videos found.")
