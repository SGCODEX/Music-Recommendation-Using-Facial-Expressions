import streamlit as st
import cv2
from deepface import DeepFace  
import numpy as np
import webbrowser
import requests
import re
import os
import time

# App config
st.set_page_config(page_title="Emotion-Based Music Player", layout="centered")
st.title("Facial Emotion Recognition App")
st.write("This app detects your facial expression, displays the predicted emotion, and plays a suitable song.")

#Footer
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

#st.title("🧠 Detected Emotion KPI")

# App state
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "show_video" not in st.session_state:
    st.session_state.show_video = False

# Function to detect emotion
def detect_emotion(frame):
    try:
        result = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
    except Exception as e:
        emotion = st.session_state.last_emotion
        print("DeepFace failed:", e)

    return frame, emotion

# ------------------------------
# 🎥 Live Camera Detection Mode
# ------------------------------
if not st.session_state.show_video:
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("📊 Current Emotion")
        emotion_placeholder = st.empty()

    cap = cv2.VideoCapture(0)
    capture = False

    with col2:
        st.subheader("📷 Live Feed")
        image_placeholder = st.empty()
        st.markdown("<br>", unsafe_allow_html=True)
        capture = st.button("🎵 Play Song on Captured Emotion")


    st.markdown("---")

    while cap.isOpened() and not capture:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (320, 240))
        frame, detected_emotion = detect_emotion(frame)
        st.session_state.last_emotion = detected_emotion

        # Update live KPI and video feed

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
        time.sleep(0.1)  # Limit refresh rate

    cap.release()
    st.session_state.show_video = True  # switch mode

# ------------------------------
# 🎧 Play Song For Detected Mood
# ------------------------------
if st.session_state.show_video:
    st.markdown("## 🎧 Now Playing Music For Your Mood")
    st.markdown(f"**Detected Mood:** `{st.session_state.last_emotion}`")

    if st.button("🔁 Detect Emotions Again"):
        st.session_state.show_video = False
        st.rerun()

    search_query = f"https://www.youtube.com/results?search_query={st.session_state.last_emotion}+background+tunes"
        
    # to fetch the search results page
    response = requests.get(search_query)
        
    # HTTP status code 200 = request was successful 
    if response.status_code != 200:
        print("Failed to retrieve YouTube search results. Status code:", response.status_code)
        
    html_content = response.text
        
    match = re.search(r'/watch\?v=([^\"]+)', html_content)
    if match:
        video_id = match.group(1)
        #video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_url = f"https://www.youtube.com/watch?v={video_id.encode('utf-8').decode('unicode_escape')}"
            
        # printing the video URL for debugging purposes
        st.video(video_url)
        print("Opening YouTube video:", video_url)




