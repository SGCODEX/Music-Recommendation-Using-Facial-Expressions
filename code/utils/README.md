# Emotion Detection Utilities

This module provides utility functions for emotion detection and music recommendation with robust error handling and logging.

## 📁 Module Structure

```
code/
├── utils/
│   └── emotion_utils.py    # Utility functions for emotion detection
└── ui_interfaces/
    └── cli_main_improved.py # Improved CLI using utilities
```

## 🔧 Functions Overview

### Camera Functions

#### `check_camera_availability(camera_index=0)`
Checks if the camera is available and accessible.

**Parameters:**
- `camera_index` (int): Index of the camera (default: 0)

**Returns:**
- `bool`: True if camera is available, False otherwise

**Example:**
```python
if check_camera_availability():
    cap = cv2.VideoCapture(0)
else:
    print("Camera not available")
```

---

### Face Detection Functions

#### `detect_faces(frame, face_cascade)`
Detects faces in a given frame using Haar Cascade classifier.

**Parameters:**
- `frame` (np.ndarray): Input video frame
- `face_cascade` (cv2.CascadeClassifier): Haar cascade classifier

**Returns:**
- `tuple`: (faces, gray_frame)
  - `faces` (list): List of detected face coordinates [(x, y, w, h), ...]
  - `gray_frame` (np.ndarray): Grayscale version of input frame

**Example:**
```python
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
faces, gray = detect_faces(frame, face_cascade)

for (x, y, w, h) in faces:
    print(f"Face detected at ({x}, {y})")
```

---

### Preprocessing Functions

#### `preprocess_face(roi_gray, target_size=(64, 64))`
Preprocesses a face region for emotion recognition model input.

**Parameters:**
- `roi_gray` (np.ndarray): Grayscale face region
- `target_size` (tuple): Target size for resizing (default: (64, 64))

**Returns:**
- `np.ndarray`: Preprocessed face with shape (1, 64, 64, 1)

**Processing Steps:**
1. Resizes to target size
2. Normalizes pixel values to [0, 1]
3. Adds batch and channel dimensions

**Example:**
```python
roi_gray = gray[y:y+h, x:x+w]
preprocessed = preprocess_face(roi_gray)
predictions = model.predict(preprocessed)
```

---

### Emotion Prediction Functions

#### `get_emotion_from_face(roi_gray, model)`
Predicts emotion from a face region using the trained model.

**Parameters:**
- `roi_gray` (np.ndarray): Grayscale face region
- `model`: Trained Keras model for emotion recognition

**Returns:**
- `str` or `None`: Predicted emotion or None if error occurs

**Supported Emotions:**
- Angry
- Disgust
- Fear
- Happy
- Sad
- Surprise
- Neutral

**Example:**
```python
emotion = get_emotion_from_face(roi_gray, model)
if emotion:
    print(f"Detected emotion: {emotion}")
```

---

### YouTube Integration Functions

#### `get_youtube_video_url(emotion)`
Gets YouTube video URL based on detected emotion.

**Parameters:**
- `emotion` (str): Detected emotion

**Returns:**
- `str` or `None`: YouTube video URL or None if error occurs

**Features:**
- 10-second timeout for requests
- Error handling for network issues
- Extracts first video from search results

**Example:**
```python
video_url = get_youtube_video_url("Happy")
if video_url:
    print(f"Found video: {video_url}")
```

#### `open_youtube_video(emotion)`
Opens YouTube video in default browser based on emotion.

**Parameters:**
- `emotion` (str): Detected emotion

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
success = open_youtube_video("Happy")
if success:
    print("Music opened in browser")
```

---

### Visualization Functions

#### `draw_emotion_on_frame(frame, x, y, w, h, emotion, color=(0, 255, 0))`
Draws emotion label and bounding box on frame.

**Parameters:**
- `frame` (np.ndarray): Input frame
- `x, y, w, h` (int): Face coordinates
- `emotion` (str): Detected emotion
- `color` (tuple): RGB color for rectangle (default: green)

**Returns:**
- `np.ndarray`: Annotated frame

**Example:**
```python
frame = draw_emotion_on_frame(frame, x, y, w, h, "Happy")
cv2.imshow("Emotion Detection", frame)
```

---

### Validation Functions

#### `validate_model_path(model_path)`
Validates if model file exists at the given path.

**Parameters:**
- `model_path` (str): Path to model file

**Returns:**
- `bool`: True if model exists, False otherwise

**Example:**
```python
if validate_model_path("model/emotion_model.hdf5"):
    model = load_model("model/emotion_model.hdf5")
```

#### `get_emotion_color(emotion)`
Gets the color code associated with an emotion for UI display.

**Parameters:**
- `emotion` (str): Emotion name

**Returns:**
- `str`: Hexadecimal color code

**Color Mappings:**
- Happy: #DFF2BF (Light green)
- Sad: #FFBABA (Light red)
- Angry: #FFAAAA (Red)
- Surprise: #FFFFBA (Yellow)
- Neutral: #E0E0E0 (Gray)
- Fear: #D0BAFF (Purple)
- Disgust: #B0FFBA (Pale green)

**Example:**
```python
color = get_emotion_color("Happy")  # Returns "#DFF2BF"
```

---

## 🚀 Complete Usage Example

```python
import cv2
from keras.models import load_model
from code.utils.emotion_utils import (
    check_camera_availability,
    validate_model_path,
    detect_faces,
    get_emotion_from_face,
    draw_emotion_on_frame,
    open_youtube_video
)

# Initialize
model_path = "code/model/fer2013_mini_XCEPTION.102-0.66.hdf5"

# Validate and load model
if not validate_model_path(model_path):
    print("Model not found!")
    exit()

model = load_model(model_path)

# Check camera
if not check_camera_availability():
    print("Camera not available!")
    exit()

# Load face cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# Start camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Detect faces
    faces, gray = detect_faces(frame, face_cascade)
    
    # Process each face
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        
        # Get emotion
        emotion = get_emotion_from_face(roi_gray, model)
        
        if emotion:
            # Draw on frame
            frame = draw_emotion_on_frame(frame, x, y, w, h, emotion)
            print(f"Detected: {emotion}")
    
    # Display
    cv2.imshow('Emotion Detection', frame)
    
    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()

# Open music based on last detected emotion
if emotion:
    open_youtube_video(emotion)
```

## 🧪 Testing

Tests are available in `tests/test_emotion_utils.py`.

Run tests:
```bash
pytest tests/test_emotion_utils.py -v
```

Run with coverage:
```bash
pytest tests/test_emotion_utils.py --cov=code/utils
```

## 📝 Logging

The module uses Python's logging module. Configure logging level in `config.py`:

```python
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## ⚠️ Error Handling

All functions include comprehensive error handling:

- **Network errors**: Timeout and connection errors for YouTube
- **Camera errors**: Graceful handling of camera unavailability
- **Model errors**: Validation and loading error handling
- **Processing errors**: Exception handling in all processing steps

## 🔍 Dependencies

- opencv-python
- keras
- tensorflow
- numpy
- requests

## 📄 License

Same as the main project.

## 🤝 Contributing

When adding new utilities:

1. Add type hints
2. Include docstrings
3. Add error handling
4. Write unit tests
5. Update this README

## 📧 Support

For issues or questions, please open an issue on GitHub.
