import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import requests
import re
import time

model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5")
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
st.markdown("""
<style>
:root {
  --primary: #dbeafe;        /* Very light blue */
  --accent: #e0f2fe;         /* Slightly lighter accent */
  --glass: rgba(255,255,255,0.30);
}
body, .stApp {
  background: linear-gradient(135deg, var(--primary), var(--accent));
  font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
}
h1, h2, .subhead {
  font-family: 'Playfair Display', 'serif';
  letter-spacing: 2px;
}
.stButton > button {
  border-radius: 10px;
  background: linear-gradient(90deg, #8fd3f4, #a6c0fe);
  color: #212529;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(41, 128, 185, 0.10);
  padding: 0.6rem 2.1rem;
  transition: 0.2s all;
}
.stButton > button:hover {
  background: linear-gradient(90deg, #60a3bc, #e0c3fc);
  color: #fff;
}
#emotion-badge {
  box-shadow: 0 2px 4px rgba(31, 38, 135, 0.13);
  font-size: 1.3rem; /* Smaller badge text */
  letter-spacing: 2px;
  border-radius: 16px;
  margin-top: 1.2rem;
  margin-bottom: 0.5rem;
  font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
}
footer {
  background: none;
  color: #222;
  text-align: center;
  margin-top: 2rem;
  font-size: 1.15rem;
  letter-spacing: 1px;
}
</style>
<link href='https://fonts.googleapis.com/css?family=Montserrat:400,700|Playfair+Display:700' rel='stylesheet' type='text/css'>
""", unsafe_allow_html=True)

st.set_page_config(page_title=" Emotion-Based Music Player", layout="centered")

st.markdown("""
<h1 style='text-align:center; color:#26283a; font-size:3.1rem; margin-bottom:0.6rem;'>
  <span style="color:#8492af">Facial Emotion</span>
  <span style="color:#6dd5ed;">Recognition</span>
  <span style='font-size: 1.4rem;'>&#128248;</span>
</h1>
<h2 style='text-align:center; color:#425c70; font-size:1.6rem;'>Your Mood, Your Music</h2>
<p class="subhead" style='text-align:center;color:#505561; margin-top:0.8rem;margin-bottom:2rem;'>Let AI read your mood & deliver a sound to soothe you!</p>
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

if not st.session_state.show_video:
    st.markdown('<div class="elegant-card" style="text-align: center;">', unsafe_allow_html=True)
    cap = cv2.VideoCapture(0)
    capture = False
    st.markdown("""
    <h2 style='margin: 0 0 1rem 0; color:#425c70;'>Emotion Detection</h2>
    <p style='color:#5c7288; margin-bottom: 1.5rem;'>Allow camera access and see your mood in real time.</p>
    """, unsafe_allow_html=True)
    emotion_placeholder = st.empty()
    image_placeholder = st.empty()
    capture = st.button(" Play Song Based on Emotion")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

    while cap.isOpened() and not capture:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (340, 260))
        frame, detected_emotion = detect_emotion(frame)
        st.session_state.last_emotion = detected_emotion

        BADGE_GRADIENTS = {
            "Happy": "linear-gradient(90deg, #f9d423, #ff4e50)",
            "Sad": "linear-gradient(90deg, #485563, #29323c)",
            "Angry": "linear-gradient(90deg, #ee0979, #ff6a00)",
            "Surprise": "linear-gradient(90deg, #a8ff78, #78ffd6)",
            "Neutral": "linear-gradient(90deg, #ece9e6, #ffffff)",
            "Fear": "linear-gradient(90deg, #ba5370, #f4e2d8)",
            "Disgust": "linear-gradient(90deg, #3ca55c, #b5ac49)"
        }
        badge_gradient = BADGE_GRADIENTS.get(detected_emotion, "linear-gradient(90deg,#ece9e6, #ffffff)")

        emotion_placeholder.markdown(
            f"""
            <div id="emotion-badge" style='margin:auto;background:{badge_gradient};width:fit-content;padding:0.2em 1.1em;'>
                {detected_emotion}
            </div>
            """, unsafe_allow_html=True
        )

        image_placeholder.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.13)
    cap.release()
    st.session_state.show_video = True

if st.session_state.show_video:
    st.markdown('<div class="elegant-card">', unsafe_allow_html=True)
    st.markdown("""
    <h2 style='text-align:center; color:#4058a5; margin-top:-0.6rem;margin-bottom:0.3rem;'>
          Curated Music For You
    </h2>
    """, unsafe_allow_html=True)
    st.markdown(
        f"<p style='font-size:1.2rem;text-align:center;'><b>Detected Mood:</b> <span style='color:#6dd5ed;'>{st.session_state.last_emotion}</span></p>",
        unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button(" Detect Again"):
        st.session_state.show_video = False
        st.rerun()

    query = f"https://www.youtube.com/results?search_query={st.session_state.last_emotion}+relaxing+music"
    response = requests.get(query)
    if response.status_code == 200:
        match = re.search(r'/watch\?v=([^"]+)', response.text)
        if match:
            video_id = match.group(1)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            st.video(video_url)
        else:
            st.error("Unable to fetch music. Please check your connection.")
    else:
        st.error("Unable to fetch music. Please check your connection.")

st.markdown("""
<footer>
  <span>Project under <a href="https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git" 
  style="color: #6dd5ed; text-decoration: none; font-weight:600;">GSSoC'25</a>
  <span style="color:#bbb;">
</footer>
""", unsafe_allow_html=True)
