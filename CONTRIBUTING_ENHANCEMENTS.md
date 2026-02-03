# Contributing Guide - Enhanced Features

This document describes the new features added to the Music Recommendation Using Facial Expressions project.

## 🎯 New Features Added

### 1. Configuration Management (`config.py`)

A centralized configuration file that contains all configurable parameters:

- **Model Configuration**: Paths and emotion labels
- **Camera Configuration**: Camera settings and frame dimensions
- **Face Detection Configuration**: Haar cascade parameters
- **YouTube Search Configuration**: Search parameters
- **UI Configuration**: Colors and themes for emotions
- **Error & Success Messages**: Standardized user feedback

**Usage:**
```python
from config import MODEL_PATH, EMOTIONS, EMOTION_COLORS

# Access configuration values
model = load_model(MODEL_PATH)
print(EMOTIONS)  # List of emotions
```

### 2. Utility Functions (`code/utils/emotion_utils.py`)

A comprehensive utility module with robust error handling:

#### Available Functions:

- **`check_camera_availability(camera_index)`**: Validates camera availability before use
- **`preprocess_face(roi_gray, target_size)`**: Preprocesses face region for model input
- **`detect_faces(frame, face_cascade)`**: Detects faces in a frame with error handling
- **`get_emotion_from_face(roi_gray, model)`**: Predicts emotion with confidence logging
- **`get_youtube_video_url(emotion)`**: Gets YouTube URL with timeout and error handling
- **`open_youtube_video(emotion)`**: Opens YouTube video in browser
- **`draw_emotion_on_frame(frame, x, y, w, h, emotion)`**: Draws annotations on frame
- **`validate_model_path(model_path)`**: Validates model file existence
- **`get_emotion_color(emotion)`**: Returns color code for emotion

**Example Usage:**
```python
from code.utils.emotion_utils import check_camera_availability, get_emotion_from_face

# Check camera before starting
if check_camera_availability():
    # Start camera
    cap = cv2.VideoCapture(0)
    
# Get emotion with error handling
emotion = get_emotion_from_face(roi_gray, model)
if emotion:
    print(f"Detected: {emotion}")
```

### 3. Unit Tests (`tests/test_emotion_utils.py`)

Comprehensive test suite for utility functions:

**Test Coverage:**
- Face preprocessing shape and normalization
- Emotion color mappings
- Model path validation
- Configuration validation
- Edge cases and error handling

**Running Tests:**
```bash
# Install dev requirements
pip install -r requirements-dev.txt

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=code/utils tests/

# Run specific test file
pytest tests/test_emotion_utils.py -v
```

### 4. Improved CLI Interface (`code/ui_interfaces/cli_main_improved.py`)

Enhanced command-line interface with:

- **Better Error Handling**: Graceful handling of all error scenarios
- **User-Friendly Messages**: Clear instructions and feedback
- **Progress Indicators**: Shows initialization steps
- **Statistics**: Displays face detection success rate
- **Improved UX**: Better visual formatting and emojis

**Running the Improved CLI:**
```bash
python code/ui_interfaces/cli_main_improved.py
```

**Features:**
- Step-by-step initialization feedback
- Clear instructions for users
- Statistics on face detection
- Proper cleanup on exit
- Keyboard interrupt handling

### 5. Development Requirements (`requirements-dev.txt`)

Separate requirements file for development dependencies:

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (includes testing tools)
pip install -r requirements-dev.txt
```

## 🔧 How to Use These Features

### For End Users:

1. **Use the Improved CLI:**
   ```bash
   python code/ui_interfaces/cli_main_improved.py
   ```
   
2. **Benefits:**
   - Better error messages
   - Clear instructions
   - More reliable camera detection
   - Improved YouTube search with timeout handling

### For Developers:

1. **Import utility functions in your code:**
   ```python
   from code.utils.emotion_utils import (
       check_camera_availability,
       get_emotion_from_face,
       open_youtube_video
   )
   ```

2. **Use configuration values:**
   ```python
   from config import EMOTIONS, MODEL_PATH, EMOTION_COLORS
   ```

3. **Run tests before committing:**
   ```bash
   pytest tests/ -v
   ```

4. **Add new tests:**
   - Add test cases in `tests/test_emotion_utils.py`
   - Follow existing test patterns
   - Ensure >80% code coverage

## 📝 Code Quality Improvements

### Error Handling
- All functions have try-catch blocks
- Meaningful error messages
- Proper logging with severity levels
- Graceful degradation

### Logging
- Uses Python's `logging` module
- Configurable log levels
- Formatted log messages with timestamps
- Separate logs for info, warnings, and errors

### Type Hints
- Added type hints for all functions
- Better IDE support and autocomplete
- Clearer function signatures

### Documentation
- Docstrings for all functions
- Parameter descriptions
- Return type documentation
- Usage examples

## 🚀 Future Enhancements

Ideas for further contributions:

1. **Spotify Integration**: Add Spotify API support
2. **Emotion History**: Track emotions over time
3. **Statistics Dashboard**: Visualize emotion patterns
4. **Multiple Music Services**: Support for Apple Music, Pandora, etc.
5. **Emotion Confidence Display**: Show prediction confidence
6. **Dark Mode**: UI theme support
7. **Settings UI**: Configuration through GUI
8. **Export Features**: Save emotion history to CSV/JSON

## 🧪 Testing Guidelines

### Writing Tests

1. **Create test file**: `tests/test_<module_name>.py`
2. **Import unittest**: `import unittest`
3. **Create test class**: Inherit from `unittest.TestCase`
4. **Name tests**: Start with `test_`
5. **Use assertions**: `assertEqual`, `assertTrue`, etc.

### Example Test:
```python
def test_preprocess_face_shape(self):
    """Test if preprocessing returns correct shape"""
    roi = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    processed = preprocess_face(roi)
    self.assertEqual(processed.shape, (1, 64, 64, 1))
```

## 📚 Additional Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [Keras Documentation](https://keras.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Logging](https://docs.python.org/3/library/logging.html)

## 🤝 Contributing

When contributing:

1. Use the utility functions from `emotion_utils.py`
2. Follow the configuration in `config.py`
3. Add tests for new features
4. Update documentation
5. Follow existing code style
6. Test thoroughly before submitting PR

## 📄 License

This contribution follows the same license as the main project.
