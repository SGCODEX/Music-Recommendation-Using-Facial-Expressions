import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import webbrowser
import requests
import re
import os
import time
import logging

# Set up logging to track errors for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App config: Set up the app's title and layout
try:
    st.set_page_config(page_title="Emotion-Based Music Player", layout="centered")
    st.title("Facial Emotion Recognition App")
    st.write("This app detects your facial expression, displays the predicted emotion, and plays a suitable song.")
except Exception as e:
    # Show error if app setup fails and stop the app
    st.error(f"Failed to initialize app configuration: {str(e)}")
    logger.error(f"App config error: {str(e)}")
    st.stop()

# Load model and face detector: Try to load the emotion model and face detection file
try:
    model = load_model("Music-Recommendation-Using-Facial-Expressions\\code\\model\\fer2013_mini_XCEPTION.102-0.66.hdf5")
    emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Check if face detector loaded correctly
    if face_cascade.empty():
        raise ValueError("Failed to load Haar cascade classifier")
except Exception as e:
    # Show error if model or face detector fails to load and stop the app
    st.error(f"Error loading model or cascade classifier: {str(e)}")
    logger.error(f"Model loading error: {str(e)}")
    st.stop()

# Footer: Add a footer with project details
try:
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
except Exception as e:
    # Show warning if footer fails to display, but keep app running
    st.warning(f"Failed to render footer: {str(e)}")
    logger.warning(f"Footer rendering error: {str(e)}")

# App state: Initialize variables to track last detected emotion and video state
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "show_video" not in st.session_state:
    st.session_state.show_video = False

# Function to detect emotion: Process a frame to find faces and predict emotion
def detect_emotion(frame):
    try:
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
    except Exception as e:
        # If emotion detection fails, log error and return last known emotion
        logger.error(f"Emotion detection error: {str(e)}")
        return frame, st.session_state.last_emotion

# Live Camera Detection Mode: Show live video feed and detect emotions
if not st.session_state.show_video:
    try:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📊 Current Emotion")
            emotion_placeholder = st.empty()

        # Camera handling: Try to access the webcam
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise ValueError("Unable to access webcam")
        except Exception as e:
            # Show error if webcam access fails and stop the app
            st.error(f"Camera initialization failed: {str(e)}")
            logger.error(f"Camera error: {str(e)}")
            st.stop()

        with col2:
            st.subheader("📷 Live Feed")
            image_placeholder = st.empty()
            st.markdown("<br>", unsafe_allow_html=True)
            capture = st.button("🎵 Play Song on Captured Emotion")

        st.markdown("---")

        # Frame processing: Process each frame from the camera
        while cap.isOpened() and not capture:
            ret, frame = cap.read()
            if not ret:
                # Show warning if frame capture fails and exit loop
                st.warning("Failed to capture frame from camera")
                logger.warning("Camera frame capture failed")
                break

            try:
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
                time.sleep(0.1)  # Limit refresh rate to avoid overloading

            except Exception as e:
                # If frame processing fails, show warning and keep running
                st.warning(f"Error processing frame: {str(e)}")
                logger.warning(f"Frame processing error: {str(e)}")
                time.sleep(0.1)
                continue

        # Release camera when done
        cap.release()

    except Exception as e:
        # General stability: Handle any errors in camera loop and stop app gracefully
        st.error(f"Error in camera processing loop: {str(e)}")
        logger.error(f"Camera loop error: {str(e)}")
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        st.stop()

    st.session_state.show_video = True

# Play Song For Detected Mood: Play a YouTube video based on the detected emotion
if st.session_state.show_video:
    try:
        st.markdown("## 🎧 Now Playing Music For Your Mood")
        st.markdown(f"**Detected Mood:** `{st.session_state.last_emotion}`")

        if st.button("🔁 Detect Emotions Again"):
            st.session_state.show_video = False
            st.rerun()

        # YouTube integration: Search for a video matching the detected emotion
        search_query = f"https://www.youtube.com/results?search_query={st.session_state.last_emotion}+background+tunes"
        
        try:
            # Try to fetch YouTube search results with a timeout
            response = requests.get(search_query, timeout=10)
            if response.status_code != 200:
                raise Exception(f"HTTP {response.status_code}")
            
            html_content = response.text
            match = re.search(r'/watch\?v=([^\"]+)', html_content)
            if not match:
                raise Exception("No video found in search results")
                
            video_id = match.group(1)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            st.video(video_url)
            logger.info(f"Playing YouTube video: {video_url}")
            
        except Exception as e:
            # Non-critical error handling: Show error if video loading fails, but keep app running
            st.error(f"Failed to load music: {str(e)}")
            logger.error(f"YouTube video error: {str(e)}")
            st.markdown("Unable to play music. Please try again.")
            
    except Exception as e:
        # General stability: Handle any errors in music playback section
        st.error(f"Error in music playback section: {str(e)}")
        logger.error(f"Music playback error: {str(e)}")