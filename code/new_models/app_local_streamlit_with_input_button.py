import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import requests
import re
import time

# Load model and labels
model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5")
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# App config
st.set_page_config(page_title="Emotion-Based Music Player", layout="centered")
st.title("Facial Emotion Recognition App")
st.write("This app detects your facial expression or lets you select one, then plays music based on your mood.")

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

# Session state setup
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "mode" not in st.session_state:
    st.session_state.mode = "input"  # can be 'input' or 'video'

# Emotion detection function
def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    emotion = st.session_state.last_emotion
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (64, 64))
        roi = roi_gray.astype("float") / 255.0
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)
        preds = model.predict(roi)[0]
        emotion = emotions[np.argmax(preds)]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        break
    return frame, emotion

# YouTube search function
def search_youtube_video(emotion):
    search_query = f"https://www.youtube.com/results?search_query={emotion}+background+tunes"
    response = requests.get(search_query)
    if response.status_code != 200:
        return None
    match = re.search(r'/watch\?v=[\w-]+', response.text)
    if match:
        return f"https://www.youtube.com{match.group()}"
    return None

# -----------------------
# 🎛️ Mode Switch Buttons
# -----------------------
col1, col2 = st.columns([1, 3])
with col1:
    if st.session_state.mode == "input":
        if st.button("🎥 Switch to Video Mode"):
            st.session_state.mode = "video"
            st.rerun()
    else:
        if st.button("🎛️ Switch to Input Mode"):
            st.session_state.mode = "input"
            st.rerun()

# -------------------------
# 🎚️ INPUT MODE (Default)
# -------------------------
if st.session_state.mode == "input":
    input = st.selectbox("🎯 Select Emotion", emotions, index=0)
    if st.button("🔍 Search Music for Selected Emotion"):
        video_url = search_youtube_video(input)
        if video_url:
            st.video(video_url)
        else:
            st.warning("Unable to find a suitable video.")

# -------------------------
# 📹 VIDEO DETECTION MODE
# -------------------------
if st.session_state.mode == "video":
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Current Emotion")
        emotion_placeholder = st.empty()

    cap = cv2.VideoCapture(0)
    capture = False

    with col2:
        st.subheader("📷 Live Feed")
        image_placeholder = st.empty()
        capture = st.button("🎵 Play Song on Captured Emotion")

    st.markdown("---")

    while cap.isOpened() and not capture:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (320, 240))
        frame, detected_emotion = detect_emotion(frame)
        st.session_state.last_emotion = detected_emotion

        emotion_colors = {
            "Happy": "#DFF2BF",
            "Sad": "#FFBABA",
            "Angry": "#FFAAAA",
            "Surprise": "#FFFFBA",
            "Neutral": "#E0E0E0",
            "Fear": "#D0BAFF",
            "Disgust": "#B0FFBA"
        }

        bg_color = emotion_colors.get(detected_emotion, "#f9fff9")
        emotion_placeholder.markdown(
            f"""
            <div style="
                display: inline-block;
                padding: 10px 24px;
                border: 2px solid #000000;
                border-radius: 14px;
                background-color: {bg_color};
                font-size: 20px;
                font-weight: 600;
                color: #333;
                text-align: center;
                margin-top: 10px;
                min-width: 120px;
            ">
                {detected_emotion}
            </div>
            """,
            unsafe_allow_html=True
        )
        image_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.1)

    cap.release()

    # Detected & now play music
    if capture:
        st.markdown("## 🎧 Now Playing Music For Your Mood")
        st.markdown(f"**Detected Mood:** `{st.session_state.last_emotion}`")
        video_url = search_youtube_video(st.session_state.last_emotion)
        if video_url:
            st.video(video_url)
        else:
            st.warning("Could not find a video for this emotion.")
