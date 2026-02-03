"""
Enhanced Streamlit interface using the new utility functions
This is an improved version of app_local_streamlit.py with better error handling
"""

import streamlit as st
import cv2
from keras.models import load_model
import numpy as np
import sys
import os
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import *
from code.utils.emotion_utils import (
    check_camera_availability,
    detect_faces,
    get_emotion_from_face,
    get_youtube_video_url,
    draw_emotion_on_frame,
    validate_model_path,
    get_emotion_color
)

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# App config
st.set_page_config(
    page_title="🎵 Emotion-Based Music Player",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        padding: 0.5rem;
        border-radius: 10px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        border-color: #FF6B6B;
    }
    .emotion-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin: 10px 0;
    }
    .stats-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎵 Music Recommendation")
    st.markdown("### Settings")
    
    # Camera settings
    camera_index = st.number_input("Camera Index", min_value=0, max_value=5, value=CAMERA_INDEX)
    
    # Emotion detection settings
    st.markdown("### Detection Settings")
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    
    # Statistics
    st.markdown("### About")
    st.info("""
    This app uses facial expression recognition to recommend music based on your mood.
    
    **Features:**
    - Real-time emotion detection
    - YouTube music recommendations
    - Detection statistics
    - Multiple emotions support
    """)
    
    st.markdown("---")
    st.markdown("⭐ [Star us on GitHub](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions)")

# Main title
st.title("🎵 Facial Emotion Recognition & Music Recommendation")
st.markdown("Detect your emotion and get personalized music recommendations!")

# Footer
st.markdown("""
    <div style="
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: #000000;
        text-align: center;
        padding: 12px;
        font-size: 14px;
        box-shadow: 0 -1px 4px rgba(0,0,0,0.1);
        border-top: 1px solid #ccc;
        z-index: 100;
    ">
        <a href="https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions" 
           style="color: #0072E3; text-decoration: underline;">
        🌟 Project by SGCODEX - Give us a star! | Open Source Programs: SWOC, IEEE-IGDTUW, GSSOC
        </a>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = DEFAULT_EMOTION
if "show_video" not in st.session_state:
    st.session_state.show_video = False
if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []
if "detection_stats" not in st.session_state:
    st.session_state.detection_stats = {
        "total_frames": 0,
        "faces_detected": 0,
        "emotions_count": {emotion: 0 for emotion in EMOTIONS}
    }

# Initialize model
@st.cache_resource
def load_emotion_model():
    """Load the emotion recognition model (cached)"""
    try:
        if not validate_model_path(MODEL_PATH):
            st.error(ERROR_MESSAGES["model_load_failed"])
            return None
        
        model = load_model(MODEL_PATH)
        st.success(SUCCESS_MESSAGES["model_loaded"])
        return model
    except Exception as e:
        st.error(f"{ERROR_MESSAGES['model_load_failed']}: {str(e)}")
        return None

# Initialize face cascade
@st.cache_resource
def load_face_cascade():
    """Load the face detection cascade (cached)"""
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + HAAR_CASCADE_PATH
        )
        if face_cascade.empty():
            st.error("Failed to load face cascade classifier")
            return None
        return face_cascade
    except Exception as e:
        st.error(f"Error loading face cascade: {str(e)}")
        return None

# Main app logic
def main():
    """Main application function"""
    
    # Load model and cascade
    model = load_emotion_model()
    face_cascade = load_face_cascade()
    
    if model is None or face_cascade is None:
        st.stop()
    
    # Camera detection mode
    if not st.session_state.show_video:
        st.markdown("### 📹 Live Emotion Detection")
        
        # Check camera availability
        if not check_camera_availability(camera_index):
            st.error(ERROR_MESSAGES["no_camera"])
            st.stop()
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 📊 Current Emotion")
            emotion_placeholder = st.empty()
            
            st.markdown("#### 📈 Statistics")
            stats_placeholder = st.empty()
        
        with col2:
            st.markdown("#### 📷 Live Camera Feed")
            image_placeholder = st.empty()
            st.markdown("<br>", unsafe_allow_html=True)
            capture_button = st.button("🎵 Capture Emotion & Play Music", type="primary")
        
        st.markdown("---")
        
        # Open camera
        cap = cv2.VideoCapture(camera_index)
        
        if not cap.isOpened():
            st.error(ERROR_MESSAGES["no_camera"])
            st.stop()
        
        # Emotion detection loop
        while cap.isOpened() and not capture_button:
            ret, frame = cap.read()
            
            if not ret:
                st.error("Failed to read from camera")
                break
            
            # Update stats
            st.session_state.detection_stats["total_frames"] += 1
            
            # Resize frame for better performance
            frame = cv2.resize(frame, (FRAME_WIDTH * 2, FRAME_HEIGHT * 2))
            
            # Detect faces and emotions
            faces, gray = detect_faces(frame, face_cascade)
            
            detected_emotion = st.session_state.last_emotion
            
            if len(faces) > 0:
                st.session_state.detection_stats["faces_detected"] += 1
                
                # Process first face
                (x, y, w, h) = faces[0]
                roi_gray = gray[y:y+h, x:x+w]
                
                # Get emotion
                emotion = get_emotion_from_face(roi_gray, model)
                
                if emotion:
                    detected_emotion = emotion
                    st.session_state.last_emotion = emotion
                    
                    # Update emotion count
                    st.session_state.detection_stats["emotions_count"][emotion] += 1
                    
                    # Add to history (keep last 50)
                    st.session_state.emotion_history.append(emotion)
                    if len(st.session_state.emotion_history) > 50:
                        st.session_state.emotion_history.pop(0)
                    
                    # Draw on frame
                    frame = draw_emotion_on_frame(frame, x, y, w, h, emotion)
            
            # Display emotion with color
            bg_color = get_emotion_color(detected_emotion)
            emotion_placeholder.markdown(
                f"""
                <div class="emotion-box" style="background-color: {bg_color};">
                    {detected_emotion}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Display statistics
            total = st.session_state.detection_stats["total_frames"]
            detected = st.session_state.detection_stats["faces_detected"]
            detection_rate = (detected / total * 100) if total > 0 else 0
            
            stats_placeholder.markdown(
                f"""
                <div class="stats-card">
                    <p><strong>Frames:</strong> {total}</p>
                    <p><strong>Faces Detected:</strong> {detected}</p>
                    <p><strong>Detection Rate:</strong> {detection_rate:.1f}%</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Display frame
            image_placeholder.image(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB),
                channels="RGB",
                use_column_width=True
            )
            
            # Small delay
            time.sleep(REFRESH_RATE)
        
        # Release camera
        cap.release()
        st.session_state.show_video = True
        st.rerun()
    
    # Music recommendation mode
    else:
        st.markdown("## 🎧 Music Recommendation")
        st.success(f"**Detected Emotion:** `{st.session_state.last_emotion}`")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔁 Detect Emotion Again", type="primary"):
                st.session_state.show_video = False
                st.rerun()
        
        with col2:
            if st.button("📊 View Statistics"):
                show_statistics()
        
        # Get YouTube video
        with st.spinner("🔍 Finding the perfect music for your mood..."):
            video_url = get_youtube_video_url(st.session_state.last_emotion)
        
        if video_url:
            st.success("🎵 Found a great match!")
            
            # Display video
            try:
                st.video(video_url)
            except Exception as e:
                st.warning("Could not embed video. Opening in browser...")
                st.markdown(f"[🎵 Click here to play music]({video_url})")
            
            # Show emotion history
            if st.session_state.emotion_history:
                st.markdown("### 📊 Your Emotion History")
                st.bar_chart({
                    emotion: st.session_state.emotion_history.count(emotion)
                    for emotion in EMOTIONS
                    if st.session_state.emotion_history.count(emotion) > 0
                })
        else:
            st.error(ERROR_MESSAGES["youtube_connection"])
            st.info("Please check your internet connection and try again.")

def show_statistics():
    """Display detailed statistics"""
    st.markdown("### 📈 Detection Statistics")
    
    stats = st.session_state.detection_stats
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Frames", stats["total_frames"])
    
    with col2:
        st.metric("Faces Detected", stats["faces_detected"])
    
    with col3:
        detection_rate = (stats["faces_detected"] / stats["total_frames"] * 100) if stats["total_frames"] > 0 else 0
        st.metric("Detection Rate", f"{detection_rate:.1f}%")
    
    # Emotion distribution
    st.markdown("### 🎭 Emotion Distribution")
    emotion_data = {
        emotion: count
        for emotion, count in stats["emotions_count"].items()
        if count > 0
    }
    
    if emotion_data:
        st.bar_chart(emotion_data)
    else:
        st.info("No emotions detected yet")

if __name__ == "__main__":
    main()
