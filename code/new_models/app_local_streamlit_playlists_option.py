import streamlit as st
import cv2
from keras.models import load_model  # Assuming you have Keras installed
import numpy as np
import webbrowser
import requests
import re
import os
import time
import pandas as pd
from datetime import datetime

# Load model and labels
model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5")
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# App config
st.set_page_config(page_title="Emotion-Based Music Player", layout="centered")
st.title("Facial Emotion Recognition App")
st.write("This app detects your facial expression, displays the predicted emotion, and plays a suitable song.")

# Initialize session state for playlist tracking
if "playlists" not in st.session_state:
    st.session_state.playlists = {}
if "current_song" not in st.session_state:
    st.session_state.current_song = None

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
        z-index: 1000;
    }
    .main-content {
        margin-bottom: 80px;
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

# Function to add song to a specific playlist
def add_song_to_playlist(playlist_name, song_data):
    if playlist_name not in st.session_state.playlists:
        st.session_state.playlists[playlist_name] = []
    st.session_state.playlists[playlist_name].append(song_data)
    st.success(f"✅ Added to {playlist_name}!")

# Function to create a new playlist
def create_new_playlist(playlist_name):
    if playlist_name not in st.session_state.playlists:
        st.session_state.playlists[playlist_name] = []
        st.success(f"✅ Created new playlist: {playlist_name}!")
    else:
        st.error(f"❌ Playlist '{playlist_name}' already exists!")

# Function to play playlist (simulate playback)
def play_playlist(playlist_name, songs):
    st.success(f"🎵 Playing {playlist_name} with {len(songs)} songs!")
    for i, song in enumerate(songs, 1):
        st.write(f"{i}. {song['song_name']} - {song['emotion']}")

# Function to delete playlist
def delete_playlist(playlist_name):
    if playlist_name in st.session_state.playlists:
        del st.session_state.playlists[playlist_name]
        st.success(f"🗑️ Deleted {playlist_name} playlist!")

# Function to delete specific song from playlist
def delete_song_from_playlist(playlist_name, song_index):
    if playlist_name in st.session_state.playlists and song_index < len(st.session_state.playlists[playlist_name]):
        deleted_song = st.session_state.playlists[playlist_name].pop(song_index)
        with st.container():
            st.success(f"🗑️ Deleted '{deleted_song['song_name']}' from {playlist_name}!")
        # If playlist becomes empty, remove it
        if len(st.session_state.playlists[playlist_name]) == 0:
            del st.session_state.playlists[playlist_name]
            with st.container():
                st.success(f"🗑️ Removed empty playlist: {playlist_name}!")

# ------------------------------
# 🎥 Live Camera Detection Mode
# ------------------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

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
        
        # Store current song data for playlist addition
        song_name = f"{st.session_state.last_emotion} Background Music"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        song_data = {
            "emotion": st.session_state.last_emotion,
            "song_name": song_name,
            "video_url": video_url,
            "timestamp": timestamp
        }
        st.session_state.current_song = song_data

# ------------------------------
# 🎵 Add to Playlist Section
# ------------------------------
if st.session_state.current_song:
    st.markdown("---")
    st.markdown("## 🎵 Add to Playlist")
    
    # Show current song info
    st.write(f"**Current Song:** {st.session_state.current_song['song_name']} ({st.session_state.current_song['emotion']})")
    
    # Add to existing playlist
    if st.session_state.playlists:
        st.write("**Add to existing playlist:**")
        playlist_names = list(st.session_state.playlists.keys())
        selected_playlist = st.selectbox("Choose playlist:", playlist_names)
        
        if st.button("➕ Add to Selected Playlist"):
            add_song_to_playlist(selected_playlist, st.session_state.current_song)
    
    # Create new playlist
    st.write("**Or create a new playlist:**")
    new_playlist_name = st.text_input("Enter new playlist name:")
    
    if st.button("📝 Create New Playlist"):
        if new_playlist_name.strip():
            create_new_playlist(new_playlist_name.strip())
            # Auto-add current song to new playlist
            add_song_to_playlist(new_playlist_name.strip(), st.session_state.current_song)
        else:
            st.error("❌ Please enter a playlist name!")

# ------------------------------
# 📋 Playlist Management Section
# ------------------------------
if st.session_state.playlists:
    st.markdown("---")
    st.markdown("## 📋 Your Playlists")
    
    for playlist_name, songs in st.session_state.playlists.items():
        with st.expander(f"🎵 {playlist_name} ({len(songs)} songs)", expanded=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**Playlist:** {playlist_name}")
                st.write(f"**Total Songs:** {len(songs)}")
                
                # Display songs in playlist with delete buttons
                st.write("**Songs:**")
                for i, song in enumerate(songs):
                    col_song1, col_song2 = st.columns([6, 1])
                    with col_song1:
                        st.write(f"**{i+1}.** {song['song_name']} - {song['emotion']}")
                    with col_song2:
                        if st.button("🗑️", key=f"delete_song_{playlist_name}_{i}", help=f"Delete '{song['song_name']}' from playlist"):
                            delete_song_from_playlist(playlist_name, i)
                            st.rerun()
            
            with col2:
                if st.button(f"▶️ Play", key=f"play_{playlist_name}"):
                    play_playlist(playlist_name, songs)
            
            with col3:
                if st.button(f"🗑️ Delete", key=f"delete_{playlist_name}"):
                    delete_playlist(playlist_name)
                    st.rerun()

# Clear all playlists button
if st.session_state.playlists:
    if st.button("🗑️ Clear All Playlists"):
        st.session_state.playlists = {}
        st.success("🗑️ All playlists cleared!")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  