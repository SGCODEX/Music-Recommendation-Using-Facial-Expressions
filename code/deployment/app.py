import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import streamlit as st
import cv2
from utils.load_model import load_trained_model
from utils.emotion_utils import detect_faces, preprocess_face, predict_emotion
from utils.youtube_search import fetch_youtube_url

model = load_trained_model()

st.set_page_config(page_title="Emotion-Based Music Player", layout="centered")
st.title("Facial Emotion Recognition App")
st.write("This app detects your facial expression and plays a suitable song.")

st.markdown("""
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
""", unsafe_allow_html=True)

if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "show_video" not in st.session_state:
    st.session_state.show_video = False

class EmotionDetector(VideoTransformerBase):
    def __init__(self):
        self.last_emotion = "Neutral"

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(gray)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi = preprocess_face(roi_gray)
            self.last_emotion = predict_emotion(model, roi)
            st.session_state.last_emotion = self.last_emotion

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, self.last_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            break

        return img

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

if st.session_state.show_video:
    st.markdown("## 🎷 Now Playing Music For Your Mood")
    st.markdown(f"**Last Detected Mood:** `{st.session_state.last_emotion}`")

    if st.button("🔁 Detect Emotions Again"):
        st.session_state.show_video = False
        st.rerun()

    video_url = fetch_youtube_url(st.session_state.last_emotion)
    if video_url:
        st.video(video_url)

