import streamlit as st
import cv2
import numpy as np
import os
import time
import textwrap
from keras.models import load_model

# --------------------------------------------------
# 1. PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="MoodTunes",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# 2. SESSION STATE
# --------------------------------------------------
if "show_songs" not in st.session_state:
    st.session_state.show_songs = False
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "frozen_emotion" not in st.session_state:
    st.session_state.frozen_emotion = "Neutral"

# --------------------------------------------------
# 3. CSS STYLING
# --------------------------------------------------
st.markdown(textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background-color: #0E1117;
    color: #FAFAFA;
}

/* Remove extra padding */
.block-container {
    padding-top: 2rem;
}

/* TOP BAR */
.top-bar {
    position: sticky;
    top: 0;
    width: 100%;
    height: 60px;
    background-color: #161B22;
    border-bottom: 1px solid #30363D;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 30px;
    z-index: 9999;
}
.website-name {
    color: white;
    font-weight: 800;
    font-size: 1.2rem;
    padding: 10px;
    margin:10px;
}
.settings-icon {
    color: #8B949E;
    font-size: 1.2rem;
    cursor: pointer;
}

/* EMOTION BOX */
.emotion-box-style {
    background-color: #262730;
    color: #FAFAFA;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    margin-top: 15px;
    border: 1px solid #30363D;
}

/* BUTTON */
.stButton > button {
    background-color: #238636;
    color: white;
    border: none;
    border-radius: 6px;
}
.stButton > button:hover {
    background-color: #2ea043;
}
</style>
"""), unsafe_allow_html=True)

# --------------------------------------------------
# 4. COMPONENTS
# --------------------------------------------------
def render_top_bar():
    st.markdown("""
    <div class="top-bar">
        <div class="website-name">MoodTunes 🎵</div>
        <div class="settings-icon">⚙️</div>
    </div>
    """, unsafe_allow_html=True)

def get_recommendations(emotion):
    db = {
        'Happy': [
            {"title": "Happy", "artist": "Pharrell Williams", "yt": "ZbZSe6N_BXs"}
        ],
        'Sad': [
            {"title": "Someone Like You", "artist": "Adele", "yt": "hLQl3WQQoQ0"}
        ],
        'Neutral': [
            {"title": "Lo-Fi Beats", "artist": "Lofi Girl", "yt": "jfKfPfyJRdk"}
        ],
        'Angry': [
            {"title": "Numb", "artist": "Linkin Park", "yt": "kXYiU_JCYtU"}
        ],
        'Fear': [
            {"title": "Thriller", "artist": "Michael Jackson", "yt": "sOnqjkJTMaA"}
        ],
        'Surprise': [
            {"title": "Firework", "artist": "Katy Perry", "yt": "QGJuMBdaqJw"}
        ],
        'Disgust': [
            {"title": "Bad Blood", "artist": "Taylor Swift", "yt": "QcIy9NiNbmo"}
        ]
    }
    return db.get(emotion, db['Neutral'])

# --------------------------------------------------
# 5. LAYOUT
# --------------------------------------------------
render_top_bar()

left_col, right_col = st.columns(2, gap="medium")

with left_col:
    st.subheader("🎥 Camera Feed")
    video_container = st.empty()
    st.markdown("---")
    emotion_container = st.empty()

with right_col:
    st.subheader("🎧 Recommendations")
    song_display_placeholder = st.empty()
    st.markdown("---")

    if st.button("🎵 Show Songs", use_container_width=True):
        st.session_state.show_songs = True
        st.session_state.frozen_emotion = st.session_state.last_emotion

# --------------------------------------------------
# 6. LOAD MODEL
# --------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "..", "model", "fer2013_mini_XCEPTION.102-0.66.hdf5")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
model = load_model(model_path, compile=False)
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# --------------------------------------------------
# 7. CAMERA LOOP
# --------------------------------------------------
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("Camera not accessible")
    st.stop()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    current_emotion = st.session_state.last_emotion

    for (x, y, w, h) in faces:
        roi = cv2.resize(gray[y:y+h, x:x+w], (64, 64))
        roi = roi.astype("float") / 255.0
        roi = np.expand_dims(roi, axis=(0, -1))
        preds = model.predict(roi, verbose=0)[0]
        current_emotion = emotions[np.argmax(preds)]
        st.session_state.last_emotion = current_emotion
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        break

    # Update camera
    video_container.image(
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
        use_container_width=True
    )

    # Update emotion
    emotion_container.markdown(
        f"<div class='emotion-box-style'><b>Detected Emotion:</b> {current_emotion}</div>",
        unsafe_allow_html=True
    )

    # Update music panel
    with song_display_placeholder.container():
        if not st.session_state.show_songs:
            st.info("Waiting for you… Click **Show Songs** to start.")
        else:
            frozen = st.session_state.frozen_emotion
            songs = get_recommendations(frozen)
            song = songs[0]  # SINGLE SONG ASSUMPTION

            st.markdown(f"### 🎵 {song['title']}")
            st.caption(song['artist'])

            # INLINE YOUTUBE PLAYER
            st.video(f"https://www.youtube.com/watch?v={song['yt']}")

    time.sleep(0.1)

cap.release()
