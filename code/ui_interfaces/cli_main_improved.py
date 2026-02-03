"""
Enhanced CLI interface with improved error handling and user experience
This is an improved version of the original cli_main.py
"""

import cv2
from keras.models import load_model
import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import *
from code.utils.emotion_utils import (
    check_camera_availability,
    detect_faces,
    get_emotion_from_face,
    open_youtube_video,
    draw_emotion_on_frame,
    validate_model_path
)

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Global variables
final_emotion = None
emotion_label = DEFAULT_EMOTION


def initialize_components():
    """
    Initialize all required components (model, face cascade, camera)
    
    Returns:
        tuple: (model, face_cascade, cap) or (None, None, None) if error occurs
    """
    print("\n🎵 Music Recommendation via Facial Expression 🎵")
    print("=" * 50)
    
    # Validate and load model
    print("\n[1/3] Loading emotion recognition model...")
    if not validate_model_path(MODEL_PATH):
        print(ERROR_MESSAGES["model_load_failed"])
        return None, None, None
    
    try:
        model = load_model(MODEL_PATH)
        print(SUCCESS_MESSAGES["model_loaded"])
    except Exception as e:
        print(f"{ERROR_MESSAGES['model_load_failed']}: {str(e)}")
        return None, None, None
    
    # Load face cascade
    print("\n[2/3] Loading face detection cascade...")
    try:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + HAAR_CASCADE_PATH
        )
        if face_cascade.empty():
            print("❌ Failed to load face cascade classifier")
            return None, None, None
        print("✅ Face cascade loaded successfully")
    except Exception as e:
        print(f"❌ Error loading face cascade: {str(e)}")
        return None, None, None
    
    # Check camera availability
    print("\n[3/3] Checking camera availability...")
    if not check_camera_availability(CAMERA_INDEX):
        print(ERROR_MESSAGES["no_camera"])
        return None, None, None
    
    # Initialize camera
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    print("\n" + "=" * 50)
    print("✅ All components initialized successfully!")
    print("=" * 50)
    
    return model, face_cascade, cap


def on_button_click(event, x, y, flags, param):
    """
    Callback function for mouse click event
    
    Args:
        event: Mouse event
        x, y: Coordinates of the click
        flags: Additional flags
        param: Additional parameters
    """
    global final_emotion, emotion_label
    
    if event == cv2.EVENT_LBUTTONDOWN:
        final_emotion = emotion_label
        print(f"\n✅ Emotion Captured: {final_emotion}")
        print("🎵 Searching for music based on your emotion...")


def main():
    """Main function to run the emotion detection and music recommendation"""
    global final_emotion, emotion_label
    
    # Initialize components
    model, face_cascade, cap = initialize_components()
    
    if model is None or face_cascade is None or cap is None:
        print("\n❌ Failed to initialize. Exiting...")
        return
    
    # Setup window and mouse callback
    window_name = 'Facial Expression Recognition'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_button_click)
    
    print("\n" + "=" * 50)
    print("📹 Camera feed started!")
    print("=" * 50)
    print("\nInstructions:")
    print("  • Position your face in front of the camera")
    print("  • Click anywhere on the window to capture emotion")
    print("  • Press 'q' to quit without capturing")
    print("=" * 50 + "\n")
    
    frame_count = 0
    face_detected_count = 0
    
    try:
        while True:
            # Read frame from camera
            ret, frame = cap.read()
            frame_count += 1
            
            if not ret:
                print("\n❌ Failed to read frame from camera")
                break
            
            # Detect faces and get emotion
            faces, gray = detect_faces(frame, face_cascade)
            
            if len(faces) > 0:
                face_detected_count += 1
                
                # Process first detected face
                (x, y, w, h) = faces[0]
                roi_gray = gray[y:y+h, x:x+w]
                
                # Get emotion
                emotion = get_emotion_from_face(roi_gray, model)
                
                if emotion:
                    emotion_label = emotion
                    
                    # Draw on frame
                    frame = draw_emotion_on_frame(frame, x, y, w, h, emotion)
            else:
                # No face detected
                if frame_count % 30 == 0:  # Show message every 30 frames
                    print(ERROR_MESSAGES["face_not_detected"])
            
            # Display frame
            cv2.imshow(window_name, frame)
            
            # Check if emotion captured
            if final_emotion is not None:
                break
            
            # Check for 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("\n⚠️ Exiting without capturing emotion...")
                cap.release()
                cv2.destroyAllWindows()
                return
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
    finally:
        # Clean up
        cap.release()
        cv2.destroyAllWindows()
    
    # Play music based on captured emotion
    if final_emotion:
        print("\n" + "=" * 50)
        print(f"🎵 Final Emotion: {final_emotion}")
        print(f"📊 Statistics: Detected faces in {face_detected_count}/{frame_count} frames")
        print("=" * 50)
        print("\n🎧 Opening music recommendation in your browser...")
        
        success = open_youtube_video(final_emotion)
        
        if success:
            print("✅ Enjoy your music! 🎵")
        else:
            print("❌ Failed to open YouTube. Please try again.")
    else:
        print("\n⚠️ No emotion captured. Please try again.")
    
    print("\n👋 Thank you for using our application!")
    print("⭐ If you liked it, please star our repository!")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
