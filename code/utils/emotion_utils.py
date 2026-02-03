"""
Utility functions for emotion detection and music recommendation
"""

import cv2
import numpy as np
import webbrowser
import requests
import re
import logging
from typing import Tuple, Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import *

# Setup logging
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def check_camera_availability(camera_index: int = CAMERA_INDEX) -> bool:
    """
    Check if camera is available
    
    Args:
        camera_index: Index of the camera to check
        
    Returns:
        bool: True if camera is available, False otherwise
    """
    cap = cv2.VideoCapture(camera_index)
    is_available = cap.isOpened()
    cap.release()
    
    if is_available:
        logger.info(SUCCESS_MESSAGES["camera_started"])
    else:
        logger.error(ERROR_MESSAGES["no_camera"])
    
    return is_available


def preprocess_face(roi_gray: np.ndarray, target_size: Tuple[int, int] = ROI_SIZE) -> np.ndarray:
    """
    Preprocess face region for emotion recognition
    
    Args:
        roi_gray: Grayscale face region
        target_size: Target size for resizing
        
    Returns:
        np.ndarray: Preprocessed face region ready for model prediction
    """
    try:
        roi = cv2.resize(roi_gray, target_size)
        roi = roi.astype("float") / 255.0
        roi = np.expand_dims(roi, axis=0)
        roi = np.expand_dims(roi, axis=-1)
        return roi
    except Exception as e:
        logger.error(f"Error in preprocessing face: {str(e)}")
        raise


def detect_faces(frame: np.ndarray, face_cascade: cv2.CascadeClassifier) -> list:
    """
    Detect faces in a frame
    
    Args:
        frame: Input frame
        face_cascade: Haar cascade classifier for face detection
        
    Returns:
        list: List of detected face coordinates [(x, y, w, h), ...]
    """
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=FACE_SCALE_FACTOR, 
            minNeighbors=FACE_MIN_NEIGHBORS
        )
        return faces, gray
    except Exception as e:
        logger.error(f"Error in face detection: {str(e)}")
        return [], None


def get_emotion_from_face(roi_gray: np.ndarray, model) -> Optional[str]:
    """
    Predict emotion from face region
    
    Args:
        roi_gray: Grayscale face region
        model: Trained emotion recognition model
        
    Returns:
        str: Predicted emotion or None if error occurs
    """
    try:
        roi = preprocess_face(roi_gray)
        preds = model.predict(roi, verbose=0)[0]
        emotion = EMOTIONS[np.argmax(preds)]
        confidence = np.max(preds)
        
        logger.info(SUCCESS_MESSAGES["emotion_detected"].format(emotion=emotion))
        logger.debug(f"Confidence: {confidence:.2%}")
        
        return emotion
    except Exception as e:
        logger.error(f"Error in emotion prediction: {str(e)}")
        return None


def get_youtube_video_url(emotion: str) -> Optional[str]:
    """
    Get YouTube video URL based on emotion
    
    Args:
        emotion: Detected emotion
        
    Returns:
        str: YouTube video URL or None if error occurs
    """
    try:
        search_query = f"{YOUTUBE_BASE_URL}{emotion}+{YOUTUBE_SEARCH_SUFFIX}"
        
        # Fetch the search results page
        response = requests.get(search_query, timeout=10)
        
        # Check if request was successful
        if response.status_code != 200:
            logger.error(f"{ERROR_MESSAGES['youtube_connection']} Status code: {response.status_code}")
            return None
        
        html_content = response.text
        
        # Extract video ID from HTML
        match = re.search(r'/watch\?v=([^\"&]+)', html_content)
        if match:
            video_id = match.group(1)
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            logger.info(SUCCESS_MESSAGES["video_opened"].format(url=video_url))
            return video_url
        else:
            logger.warning(ERROR_MESSAGES["no_video_found"])
            return None
            
    except requests.Timeout:
        logger.error("Request timed out while connecting to YouTube")
        return None
    except requests.RequestException as e:
        logger.error(f"{ERROR_MESSAGES['youtube_connection']}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in YouTube search: {str(e)}")
        return None


def open_youtube_video(emotion: str) -> bool:
    """
    Open YouTube video in browser based on emotion
    
    Args:
        emotion: Detected emotion
        
    Returns:
        bool: True if successful, False otherwise
    """
    video_url = get_youtube_video_url(emotion)
    
    if video_url:
        try:
            webbrowser.open(video_url)
            return True
        except Exception as e:
            logger.error(f"Error opening browser: {str(e)}")
            return False
    
    return False


def draw_emotion_on_frame(frame: np.ndarray, x: int, y: int, w: int, h: int, 
                         emotion: str, color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
    """
    Draw rectangle and emotion label on frame
    
    Args:
        frame: Input frame
        x, y, w, h: Face coordinates
        emotion: Detected emotion
        color: Rectangle color (BGR)
        
    Returns:
        np.ndarray: Frame with annotations
    """
    try:
        # Draw rectangle around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        # Draw emotion label
        cv2.putText(
            frame, 
            emotion, 
            (x, y-10), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.9, 
            (36, 255, 12), 
            2
        )
        
        return frame
    except Exception as e:
        logger.error(f"Error drawing on frame: {str(e)}")
        return frame


def validate_model_path(model_path: str) -> bool:
    """
    Validate if model file exists
    
    Args:
        model_path: Path to model file
        
    Returns:
        bool: True if model exists, False otherwise
    """
    if not os.path.exists(model_path):
        logger.error(f"{ERROR_MESSAGES['model_load_failed']} Path: {model_path}")
        return False
    
    logger.info(SUCCESS_MESSAGES["model_loaded"])
    return True


def get_emotion_color(emotion: str) -> str:
    """
    Get color associated with emotion
    
    Args:
        emotion: Emotion name
        
    Returns:
        str: Hex color code
    """
    return EMOTION_COLORS.get(emotion, "#E0E0E0")
