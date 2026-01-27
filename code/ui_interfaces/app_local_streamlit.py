import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import webbrowser
import requests
import re
import os
import time

# =========================================================
# 📄 App Configuration
# =========================================================
st.set_page_config(
    page_title="Emotion-Based Music Recommendation",
    page_icon="🎵",
    layout="centered"
)

st.title("🎵 Emotion-Based Music Recommendation System")
st.write(
    "This application detects your facial emotion in real time using your webcam "
    "and recommends music that matches your current mood."
)

st.markdown(
    """
    ### 🧭 How to Use
    1. Allow webcam access when prompted  
    2. Look naturally at the camera  
    3. Click **Capture Emotion & Play Music**  
    4. Enjoy music recommendations based on your mood 🎧
    """
)

st.markdown("---")

# =========================================================
# ⚙️ Sidebar (UX Improvement)
# =========================================================
st.sidebar.header("⚙️ Application Settings")
st.sidebar.info(
    "Ensure your webcam is connected and working properly before starting emotion detection."
)

# =========================================================
# 🤖 Load Model and Resources
# =========================================================
MODEL_PATH = "code/model/fer2013_mini_XCEPTION.102-0.66.hdf5"

if not os.path.exists(MODEL_PATH):
    st.error("❌ Emotion model file not found. Please check the model path.")
    st.stop()

model = load_model(MODEL_PATH)

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# =========================================================
# 🧠 Session State Initialization
# =========================================================
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"

if "show_video" not in st.session_state:
    st.session_state.show_video = False

# =========================================================
# 😐 Emotion Detection Logic (UNCHANGED)
# =========================================================
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

        preds = model.predict(roi, verbose=0)[0]
        emotion = emotions[np.argmax(preds)]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            emotion,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (36, 255, 12),
            2
        )
        break

    return frame, emotion

# =========================================================
# 🎥 Live Camera Detection Mode
# =========================================================
if not st.session_state.show_video:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Current Emotion")
        emotion_placeholder = st.empty()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Unable to access webcam. Please check camera permissions.")
        st.stop()

    capture = False

    with col2:
        st.subheader("📷 Live Feed")
        image_placeholder = st.empty()
        st.markdown("<br>", unsafe_allow_html=True)
        capture = st.button("🎵 Capture Emotion & Play Music")

    st.markdown("---")

    while cap.isOpened() and not capture:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Unable to read frame from webcam.")
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
                padding: 12px 24px;
                border-radius: 14px;
                background-color: {bg_color};
                font-size: 20px;
                font-weight: 600;
                text-align: center;
            ">
                {detected_emotion}
            </div>
            """,
            unsafe_allow_html=True
        )

        image_placeholder.image(
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
            channels="RGB"
        )

        time.sleep(0.1)

    cap.release()
    st.session_state.show_video = True

# =========================================================
# 🎧 Music Recommendation
# =========================================================
if st.session_state.show_video:
    st.subheader("🎧 Music Recommendation")
    st.markdown(f"**Detected Mood:** `{st.session_state.last_emotion}`")

    if st.button("🔁 Detect Emotion Again"):
        st.session_state.show_video = False
        st.rerun()

    search_query = (
        f"https://www.youtube.com/results?"
        f"search_query={st.session_state.last_emotion}+music"
    )

    response = requests.get(search_query)
    if response.status_code != 200:
        st.error("❌ Failed to fetch YouTube recommendations.")
        st.stop()

    match = re.search(r'/watch\?v=([^\"]+)', response.text)
    if match:
        video_id = match.group(1)
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        st.video(video_url)
    else:
        st.warning("⚠️ No suitable music found for this emotion.")

# =========================================================
# 🔻 Footer
# =========================================================
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #ccc;
    }
    </style>

    <div class="footer">
        <a href="https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions"
           target="_blank">
           Project by SGCODEX · Please ⭐ the repo if you like it
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
