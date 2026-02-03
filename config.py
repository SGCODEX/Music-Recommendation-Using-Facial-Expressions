"""
Configuration file for Music Recommendation Using Facial Expressions
This file contains all configurable parameters for the application
"""

import os

# Model Configuration
MODEL_PATH = "code/model/fer2013_mini_XCEPTION.102-0.66.hdf5"
EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Camera Configuration
CAMERA_INDEX = 0  # Default camera index (0 for built-in webcam)
FRAME_WIDTH = 320
FRAME_HEIGHT = 240

# Face Detection Configuration
HAAR_CASCADE_PATH = 'haarcascade_frontalface_default.xml'
FACE_SCALE_FACTOR = 1.3
FACE_MIN_NEIGHBORS = 5

# Model Input Configuration
ROI_SIZE = (64, 64)  # Size for emotion recognition model input

# YouTube Search Configuration
YOUTUBE_SEARCH_SUFFIX = "background tunes"  # Suffix added to emotion for search
YOUTUBE_BASE_URL = "https://www.youtube.com/results?search_query="

# UI Configuration
EMOTION_COLORS = {
    "Happy": "#DFF2BF",
    "Sad": "#FFBABA",
    "Angry": "#FFAAAA",
    "Surprise": "#FFFFBA",
    "Neutral": "#E0E0E0",
    "Fear": "#D0BAFF",
    "Disgust": "#B0FFBA"
}

# Application Settings
REFRESH_RATE = 0.1  # Delay between frames in seconds
DEFAULT_EMOTION = "Neutral"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Error Messages
ERROR_MESSAGES = {
    "no_camera": "❌ Camera not found. Please check your webcam connection.",
    "model_load_failed": "❌ Failed to load emotion recognition model.",
    "youtube_connection": "❌ Failed to connect to YouTube. Please check your internet connection.",
    "no_video_found": "❌ No video found for the given emotion.",
    "face_not_detected": "⚠️ No face detected. Please ensure your face is visible to the camera."
}

# Success Messages
SUCCESS_MESSAGES = {
    "camera_started": "✅ Camera started successfully",
    "model_loaded": "✅ Model loaded successfully",
    "emotion_detected": "✅ Emotion detected: {emotion}",
    "video_opened": "✅ Opening video: {url}"
}
