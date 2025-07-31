import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import requests
import re
import time

# Load model and labels
model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5", compile=False)
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Streamlit App Config
st.set_page_config(page_title="Emotion-Based Music Player", layout="centered")
st.title("Facial Emotion Recognition App")
st.write("This app detects your facial expression, displays the predicted emotion, and plays a suitable song.")

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

# Session State
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "show_video" not in st.session_state:
    st.session_state.show_video = False

# Emotion Detection Function
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

# --------------------------
# 👁️ Emotion Detection Mode
# --------------------------
if not st.session_state.show_video:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📊 Current Emotion")
        emotion_placeholder = st.empty()
    with col2:
        st.subheader("📷 Live Feed")
        image_placeholder = st.empty()
        st.markdown("<br>", unsafe_allow_html=True)
        capture = st.button("🎵 Play Song on Captured Emotion")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("Could not open webcam.")
    else:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (320, 240))
            frame, detected_emotion = detect_emotion(frame)
            st.session_state.last_emotion = detected_emotion

            # Emotion color mapping
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

            if capture:
                cap.release()
                st.session_state.show_video = True
                st.rerun()

            time.sleep(0.1)

# --------------------------
# 🎧 YouTube Music Section
# --------------------------
if st.session_state.show_video:
    st.markdown("## 🎶 Playing music based on your detected emotion")
    st.markdown(f"**Detected emotion:** `{st.session_state.last_emotion}`")

    if st.button("🔄 Detect emotion again"):
        with st.spinner("Switching back to emotion detection..."):
            time.sleep(1.6)
            st.session_state.show_video = False
            st.info("You're now in emotion detection mode.")
            st.rerun()

    search_query = f"https://www.youtube.com/results?search_query={st.session_state.last_emotion}+background+music"

    with st.spinner("Loading video suggestions..."):
        response = requests.get(search_query)
        if response.status_code != 200:
            st.error(f"Failed to fetch videos (status: {response.status_code})")
        else:
            html_content = response.text
            match = re.search(r'/watch\?v=([^\"]+)', html_content)
            if match:
                video_id = match.group(1)
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                st.success("Here's a song based on your mood!")
                st.video(video_url)
            else:
                st.warning("No video found on YouTube for your emotion.")