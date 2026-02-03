"""
Unit tests for emotion detection utilities
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from code.utils.emotion_utils import (
    preprocess_face,
    get_emotion_color,
    validate_model_path
)
from config import EMOTIONS, EMOTION_COLORS, ROI_SIZE


class TestEmotionUtils(unittest.TestCase):
    """Test cases for emotion utility functions"""
    
    def test_preprocess_face_shape(self):
        """Test if face preprocessing returns correct shape"""
        # Create a dummy grayscale face region
        roi_gray = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        
        # Preprocess the face
        processed = preprocess_face(roi_gray)
        
        # Check shape: (1, 64, 64, 1)
        self.assertEqual(processed.shape, (1, ROI_SIZE[0], ROI_SIZE[1], 1))
        
    def test_preprocess_face_normalization(self):
        """Test if face preprocessing normalizes values to [0, 1]"""
        roi_gray = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
        processed = preprocess_face(roi_gray)
        
        # Check if values are in [0, 1] range
        self.assertTrue(np.all(processed >= 0))
        self.assertTrue(np.all(processed <= 1))
        
    def test_get_emotion_color_valid(self):
        """Test if valid emotions return correct colors"""
        for emotion in EMOTIONS:
            color = get_emotion_color(emotion)
            self.assertIn(color, EMOTION_COLORS.values())
            
    def test_get_emotion_color_invalid(self):
        """Test if invalid emotion returns default color"""
        color = get_emotion_color("InvalidEmotion")
        self.assertEqual(color, "#E0E0E0")
        
    def test_validate_model_path_invalid(self):
        """Test if invalid model path returns False"""
        invalid_path = "/invalid/path/to/model.hdf5"
        result = validate_model_path(invalid_path)
        self.assertFalse(result)
        
    def test_emotions_list(self):
        """Test if EMOTIONS list has expected emotions"""
        expected_emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.assertEqual(EMOTIONS, expected_emotions)
        
    def test_emotion_colors_completeness(self):
        """Test if all emotions have color mappings"""
        for emotion in EMOTIONS:
            self.assertIn(emotion, EMOTION_COLORS)


class TestEmotionDetection(unittest.TestCase):
    """Test cases for emotion detection workflow"""
    
    def test_roi_size_configuration(self):
        """Test if ROI size is properly configured"""
        self.assertEqual(ROI_SIZE, (64, 64))
        
    def test_preprocess_with_different_sizes(self):
        """Test preprocessing with various input sizes"""
        sizes = [(50, 50), (100, 100), (200, 200), (300, 300)]
        
        for size in sizes:
            roi_gray = np.random.randint(0, 255, size, dtype=np.uint8)
            processed = preprocess_face(roi_gray)
            
            # All should result in same output shape
            self.assertEqual(processed.shape, (1, ROI_SIZE[0], ROI_SIZE[1], 1))


if __name__ == '__main__':
    unittest.main()
