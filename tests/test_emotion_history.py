"""
Tests for emotion history tracker
"""

import unittest
import os
import json
from datetime import datetime, timedelta
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from code.utils.emotion_history import EmotionHistoryTracker


class TestEmotionHistoryTracker(unittest.TestCase):
    """Test cases for EmotionHistoryTracker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test_emotion_history.json"
        self.tracker = EmotionHistoryTracker(self.test_file)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        csv_file = "emotion_history.csv"
        if os.path.exists(csv_file):
            os.remove(csv_file)
    
    def test_add_emotion(self):
        """Test adding emotions"""
        self.tracker.add_emotion("Happy", 0.95)
        self.assertEqual(len(self.tracker), 1)
        
        self.tracker.add_emotion("Sad", 0.85)
        self.assertEqual(len(self.tracker), 2)
    
    def test_save_and_load(self):
        """Test saving and loading history"""
        self.tracker.add_emotion("Happy", 0.95)
        self.tracker.add_emotion("Neutral", 0.87)
        
        # Save
        result = self.tracker.save_history()
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_file))
        
        # Load in new tracker
        new_tracker = EmotionHistoryTracker(self.test_file)
        self.assertEqual(len(new_tracker), 2)
    
    def test_get_emotion_counts(self):
        """Test emotion counting"""
        self.tracker.add_emotion("Happy", 0.95)
        self.tracker.add_emotion("Happy", 0.92)
        self.tracker.add_emotion("Sad", 0.85)
        
        counts = self.tracker.get_emotion_counts()
        self.assertEqual(counts["Happy"], 2)
        self.assertEqual(counts["Sad"], 1)
    
    def test_get_most_common_emotion(self):
        """Test finding most common emotion"""
        self.tracker.add_emotion("Happy", 0.95)
        self.tracker.add_emotion("Happy", 0.92)
        self.tracker.add_emotion("Sad", 0.85)
        
        most_common = self.tracker.get_most_common_emotion()
        self.assertEqual(most_common, "Happy")
    
    def test_get_recent_emotions(self):
        """Test getting recent emotions"""
        for i in range(15):
            self.tracker.add_emotion("Happy", 0.9)
        
        recent = self.tracker.get_recent_emotions(5)
        self.assertEqual(len(recent), 5)
    
    def test_get_statistics(self):
        """Test statistics generation"""
        self.tracker.add_emotion("Happy", 0.95)
        self.tracker.add_emotion("Sad", 0.85)
        self.tracker.add_emotion("Happy", 0.90)
        
        stats = self.tracker.get_statistics()
        
        self.assertEqual(stats["total_detections"], 3)
        self.assertEqual(stats["most_common"], "Happy")
        self.assertEqual(stats["unique_emotions"], 2)
        self.assertAlmostEqual(stats["average_confidence"], 0.9, places=2)
    
    def test_export_to_csv(self):
        """Test CSV export"""
        self.tracker.add_emotion("Happy", 0.95)
        self.tracker.add_emotion("Sad", 0.85)
        
        result = self.tracker.export_to_csv()
        self.assertTrue(result)
        self.assertTrue(os.path.exists("emotion_history.csv"))
    
    def test_clear_history(self):
        """Test clearing history"""
        self.tracker.add_emotion("Happy", 0.95)
        self.tracker.add_emotion("Sad", 0.85)
        
        self.assertEqual(len(self.tracker), 2)
        
        self.tracker.clear_history()
        self.assertEqual(len(self.tracker), 0)
    
    def test_get_emotions_by_date(self):
        """Test filtering by date"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        self.tracker.add_emotion("Happy", 0.95)
        self.tracker.add_emotion("Sad", 0.85)
        
        emotions = self.tracker.get_emotions_by_date(today)
        self.assertEqual(len(emotions), 2)
    
    def test_empty_tracker(self):
        """Test operations on empty tracker"""
        stats = self.tracker.get_statistics()
        self.assertEqual(stats["total_detections"], 0)
        self.assertIsNone(stats["most_common"])
        
        most_common = self.tracker.get_most_common_emotion()
        self.assertIsNone(most_common)
        
        recent = self.tracker.get_recent_emotions(10)
        self.assertEqual(len(recent), 0)


class TestEmotionHistoryAdvanced(unittest.TestCase):
    """Advanced test cases for EmotionHistoryTracker"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test_emotion_history_advanced.json"
        self.tracker = EmotionHistoryTracker(self.test_file)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_emotion_trend(self):
        """Test emotion trend over days"""
        # Add emotions for different days
        for i in range(7):
            timestamp = datetime.now() - timedelta(days=i)
            self.tracker.add_emotion("Happy", 0.9, timestamp)
        
        trend = self.tracker.get_emotion_trend(days=7)
        self.assertIn("Happy", trend)
        self.assertEqual(len(trend["Happy"]), 7)
    
    def test_emotion_duration(self):
        """Test emotion duration calculation"""
        now = datetime.now()
        
        self.tracker.add_emotion("Happy", 0.9, now)
        self.tracker.add_emotion("Happy", 0.9, now + timedelta(seconds=10))
        self.tracker.add_emotion("Happy", 0.9, now + timedelta(seconds=20))
        
        durations = self.tracker.get_emotion_duration()
        self.assertIn("Happy", durations)
        self.assertAlmostEqual(durations["Happy"], 10.0, places=0)
    
    def test_large_history(self):
        """Test with large history"""
        # Add many emotions
        for i in range(1000):
            emotion = ["Happy", "Sad", "Angry"][i % 3]
            self.tracker.add_emotion(emotion, 0.9)
        
        self.assertEqual(len(self.tracker), 1000)
        
        stats = self.tracker.get_statistics()
        self.assertEqual(stats["total_detections"], 1000)


if __name__ == '__main__':
    unittest.main()
