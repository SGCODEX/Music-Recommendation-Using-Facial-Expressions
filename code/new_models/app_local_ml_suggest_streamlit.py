import streamlit as st
import cv2
from keras.models import load_model
from keras.optimizers import Adam 
import numpy as np
import webbrowser
import requests
import re
import os
import time
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import NearestNeighbors
import pandas as pd
# Load model and labels
model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5", compile=False)

emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
if "last_level" not in st.session_state:
    st.session_state.last_level = 50 
if "show_video" not in st.session_state:
    st.session_state.show_video = False
# ML songs recommender
@st.cache_resource 
def load_model_csv(csv_file):
    df = pd.read_csv(csv_file)
    le = LabelEncoder()
    df['EmotionLabel'] = le.fit_transform(df['Emotion'])
    X = df[['EmotionLabel', 'level_of_emotion']].astype(float).values
    model = NearestNeighbors(n_neighbors=30)
    model.fit(X)
    return model, df, le
@st.cache_data
def recommend_songs(_model, df, le, emotion, level, n_recs=7):
    try:
        emotion_code = le.transform([emotion])[0]
        distances, indices = _model.kneighbors([[emotion_code, level]], n_neighbors=n_recs)
        return df.iloc[indices[0]]
    except Exception as e:
        st.warning(f"Recommendation error: {e}")
        return df.sample(n=n_recs)

# Function to detect emotion
def detect_emotion(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    emotion = st.session_state.last_emotion
    level = st.session_state.last_level
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (64, 64))
        roi = roi_gray.astype("float") / 255.0
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)
        preds = model.predict(roi)[0]
        emotion = emotions[np.argmax(preds)]
        confidence=np.max(preds)
        level=int(confidence*100)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
        break
    return frame, emotion ,level

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
        frame, detected_emotion, detected_level= detect_emotion(frame)
        st.session_state.last_emotion = detected_emotion
        st.session_state.last_level = detected_level
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
                {detected_emotion} (Level {detected_level})
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
# if st.session_state.show_video:
#     st.markdown("## 🎧 Now Playing Music For Your Mood")
#     st.markdown(f"**Detected Mood:** `{st.session_state.last_emotion}`")

#     if st.button("🔁 Detect Emotions Again"):
#         st.session_state.show_video = False
#         st.rerun()

#     search_query = f"https://www.youtube.com/results?search_query={st.session_state.last_emotion}+background+tunes"
        
#     # to fetch the search results page
#     response = requests.get(search_query)
        
#     # HTTP status code 200 = request was successful 
#     if response.status_code != 200:
#         print("Failed to retrieve YouTube search results. Status code:", response.status_code)
        
#     html_content = response.text
        
#     match = re.search(r'/watch\?v=([^\"]+)', html_content)
#     if match:
#         video_id = match.group(1)
#         #video_url = f"https://www.youtube.com/watch?v={video_id}"
#         video_url = f"https://www.youtube.com/watch?v={video_id.encode('utf-8').decode('unicode_escape')}"
            
#         # printing the video URL for debugging purposes
#         st.video(video_url)
#         print("Opening YouTube video:", video_url)
#Recommendation UI
if st.session_state.show_video:
    st.markdown("---")
    st.header("🎧 Song Recommendations Based on Your Mood")
    emo = st.session_state.last_emotion
    lvl = st.session_state.last_level
    st.success(f"Detected: **{emo}** | Confidence Level: **{lvl}**")

    model, df, le = load_model_csv(r"code\new_models\emotion_songs.csv")
    results = recommend_songs(model, df, le, emo, lvl, n_recs=7)

    song_names = results['Song Title'].tolist()
    links = results['YouTube Link'].tolist()
    levels = results['level_of_emotion'].tolist()

    st.subheader("🎶 Recommended Songs:")
    selected_song = st.selectbox("Select a song to play", song_names)

    if selected_song:
        index = song_names.index(selected_song)
        st.markdown(f"**Emotion Level:** {levels[index]}")
        st.video(links[index])

    if st.button("🔁 Detect Again"):
        st.session_state.show_video = False
        st.rerun()


