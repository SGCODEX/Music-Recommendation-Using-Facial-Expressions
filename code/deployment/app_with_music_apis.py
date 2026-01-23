"""
Enhanced Emotion-Based Music Recommendation App with Spotify & YouTube Integration
Streamlit UI with real music streaming capabilities
"""

from streamlit_webrtc import webrtc_streamer, VideoTransformerBase  # type: ignore
import streamlit as st
import cv2
from keras.models import load_model  # type: ignore
import numpy as np
import os
import sys

# Add music_apis to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from music_apis import EmotionMapper, SpotifyMusicAPI, YouTubeMusicAPI
except ImportError:
    st.error("❌ Error: Could not import music_apis module. Please check your installation.")
    st.stop()

# Load model and labels
model = load_model("code/model/fer2013_mini_XCEPTION.102-0.66.hdf5")
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # type: ignore

# Initialize API clients
emotion_mapper = EmotionMapper()

# Initialize with environment variables or empty (will use fallback methods)
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID', '')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '')
youtube_api_key = os.getenv('YOUTUBE_API_KEY', '')

spotify_api = SpotifyMusicAPI(spotify_client_id, spotify_client_secret)
youtube_api = YouTubeMusicAPI(youtube_api_key)

# App config
st.set_page_config(
    page_title="🎵 Emotion-Based Music Player", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .emotion-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 1rem 0;
    }
    .track-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .track-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    .music-source-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: bold;
        margin-right: 0.5rem;
    }
    .spotify-badge {
        background: #1DB954;
        color: white;
    }
    .youtube-badge {
        background: #FF0000;
        color: white;
    }
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🎵 Emotion-Based Music Recommendation</h1>
    <p>Let AI detect your mood and discover the perfect soundtrack</p>
</div>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")
    
    st.subheader("🎵 Music Sources")
    use_spotify = st.checkbox("Use Spotify", value=True, help="Get recommendations from Spotify")
    use_youtube = st.checkbox("Use YouTube", value=True, help="Get videos from YouTube")
    
    st.subheader("🔑 API Credentials (Optional)")
    with st.expander("Spotify Credentials"):
        st.info("Get your credentials from: https://developer.spotify.com/dashboard")
        spotify_id_input = st.text_input("Client ID", value=spotify_client_id, type="password")
        spotify_secret_input = st.text_input("Client Secret", value=spotify_client_secret, type="password")
        if st.button("Update Spotify Credentials"):
            spotify_api.client_id = spotify_id_input
            spotify_api.client_secret = spotify_secret_input
            st.success("✅ Credentials updated!")
    
    with st.expander("YouTube API Key"):
        st.info("Get your API key from: https://console.cloud.google.com/")
        youtube_key_input = st.text_input("API Key", value=youtube_api_key, type="password")
        if st.button("Update YouTube Key"):
            youtube_api.api_key = youtube_key_input
            st.success("✅ API key updated!")
    
    st.subheader("🎚️ Preferences")
    num_recommendations = st.slider("Number of recommendations", 5, 20, 10)
    auto_play = st.checkbox("Auto-play first recommendation", value=False)

# App state
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "Neutral"
if "show_music" not in st.session_state:
    st.session_state.show_music = False
if "recommendations" not in st.session_state:
    st.session_state.recommendations = {'spotify': [], 'youtube': []}

# Streamlit WebRTC Video Transformer
class EmotionDetector(VideoTransformerBase):
    def __init__(self):
        self.last_emotion = "Neutral"

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (64, 64))
            roi = roi_gray.astype("float") / 255.0
            roi = np.expand_dims(roi, axis=0)
            roi = np.expand_dims(roi, axis=-1)
            preds = model.predict(roi)[0]
            self.last_emotion = emotions[np.argmax(preds)]
            st.session_state.last_emotion = self.last_emotion

            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, self.last_emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
            break

        return img

# Main App Flow
if not st.session_state.show_music:
    st.markdown("## 📷 Emotion Detection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("👇 Allow camera access to detect your emotion")
        ctx = webrtc_streamer(
            key="emotion",
            video_transformer_factory=EmotionDetector,
            rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
            media_stream_constraints={"video": True, "audio": False}
        )
    
    with col2:
        st.markdown("### 📊 Current Emotion")
        st.markdown(f'<div class="emotion-badge">{st.session_state.last_emotion}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🎵 Get Music Recommendations", type="primary"):
            st.session_state.show_music = True
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 💡 Tip")
        st.info("Look at the camera for a few seconds to detect your emotion, then click the button above to get personalized music recommendations!")

else:
    # Music Recommendation View
    emotion = st.session_state.last_emotion
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## 🎧 Music for your **{emotion}** mood")
    with col2:
        if st.button("🔄 Detect Again"):
            st.session_state.show_music = False
            st.rerun()
    
    # Get emotion parameters
    emotion_params = emotion_mapper.get_spotify_params(emotion)
    mood_description = emotion_mapper.get_mood_description(emotion)
    
    st.markdown(f"*Finding {mood_description} tracks for you...*")
    
    # Create tabs for different sources
    tabs = []
    if use_spotify:
        tabs.append("🎵 Spotify")
    if use_youtube:
        tabs.append("📹 YouTube")
    
    if not tabs:
        st.error("⚠️ Please enable at least one music source in the sidebar!")
    else:
        tab_views = st.tabs(tabs)
        
        # Spotify Tab
        if use_spotify:
            with tab_views[0]:
                with st.spinner("🔍 Searching Spotify..."):
                    # Get Spotify recommendations
                    spotify_tracks = spotify_api.get_recommendations(
                        emotion_params, 
                        limit=num_recommendations
                    )
                    
                    if not spotify_tracks:
                        st.warning("⚠️ Could not fetch Spotify recommendations. Please check your API credentials in the sidebar.")
                        # Try searching instead
                        spotify_tracks = spotify_api.search_tracks(
                            mood_description,
                            limit=num_recommendations
                        )
                
                if spotify_tracks:
                    st.success(f"✅ Found {len(spotify_tracks)} tracks on Spotify!")
                    
                    # Display tracks
                    for idx, track in enumerate(spotify_tracks):
                        with st.container():
                            col1, col2, col3 = st.columns([1, 3, 1])
                            
                            with col1:
                                if track['album_art']:
                                    st.image(track['album_art'], width=100)
                            
                            with col2:
                                st.markdown(f"**{track['name']}**")
                                st.markdown(f"*{track['artist']}*")
                                st.markdown(f"Album: {track['album']}")
                            
                            with col3:
                                if track['preview_url']:
                                    st.audio(track['preview_url'])
                                st.markdown(f"[Open in Spotify]({track['spotify_url']})", unsafe_allow_html=True)
                            
                            st.markdown("---")
                            
                            # Auto-play first track
                            if idx == 0 and auto_play and track['preview_url']:
                                st.info("🎵 Auto-playing preview...")
                else:
                    st.error("❌ No Spotify tracks found. Please check your API credentials.")
        
        # YouTube Tab
        if use_youtube:
            tab_idx = 1 if use_spotify else 0
            with tab_views[tab_idx]:
                with st.spinner("🔍 Searching YouTube..."):
                    # Get YouTube videos
                    youtube_videos = youtube_api.search_by_emotion(
                        emotion,
                        max_results=num_recommendations
                    )
                
                if youtube_videos:
                    st.success(f"✅ Found {len(youtube_videos)} videos on YouTube!")
                    
                    # Display first video prominently
                    if auto_play and youtube_videos:
                        st.markdown("### 🎬 Now Playing")
                        st.video(youtube_videos[0]['video_url'])
                        st.markdown(f"**{youtube_videos[0]['title']}**")
                        st.markdown(f"*{youtube_videos[0]['channel']}*")
                        st.markdown("---")
                    
                    # Display other videos in grid
                    st.markdown("### 📋 More Recommendations")
                    
                    for idx, video in enumerate(youtube_videos[1:] if auto_play else youtube_videos):
                        with st.container():
                            col1, col2 = st.columns([1, 2])
                            
                            with col1:
                                st.image(video['thumbnail'], use_container_width=True)
                            
                            with col2:
                                st.markdown(f"**{video['title'][:60]}...**" if len(video['title']) > 60 else f"**{video['title']}**")
                                st.markdown(f"*{video['channel']}*")
                                
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.markdown(f"[▶️ Watch]({video['video_url']})")
                                with col_b:
                                    if st.button(f"Play #{idx+1}", key=f"play_{idx}"):
                                        st.video(video['video_url'])
                            
                            st.markdown("---")
                else:
                    st.error("❌ No YouTube videos found.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #666;'>
    <p>🎵 <strong>Emotion-Based Music Recommendation System</strong></p>
    <p>Powered by Spotify Web API & YouTube Data API</p>
    <p style='font-size: 0.9rem;'>
        <a href="https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions" target="_blank">⭐ Star on GitHub</a> | 
        <a href="https://developer.spotify.com/documentation/web-api" target="_blank">Spotify API Docs</a> | 
        <a href="https://developers.google.com/youtube/v3" target="_blank">YouTube API Docs</a>
    </p>
</div>
""", unsafe_allow_html=True)
