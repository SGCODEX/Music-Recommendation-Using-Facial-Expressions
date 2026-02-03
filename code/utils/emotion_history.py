"""
Emotion History Tracker
Track and analyze emotion patterns over time
"""

import json
import csv
from datetime import datetime
from typing import List, Dict, Optional
import os


class EmotionHistoryTracker:
    """Track and analyze emotion detection history"""
    
    def __init__(self, history_file: str = "emotion_history.json"):
        """
        Initialize the emotion history tracker
        
        Args:
            history_file: Path to the history file
        """
        self.history_file = history_file
        self.history: List[Dict] = []
        self.load_history()
    
    def add_emotion(self, emotion: str, confidence: float = 0.0, 
                   timestamp: Optional[datetime] = None) -> None:
        """
        Add an emotion detection to history
        
        Args:
            emotion: Detected emotion
            confidence: Confidence score
            timestamp: Time of detection (default: now)
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        entry = {
            "emotion": emotion,
            "confidence": confidence,
            "timestamp": timestamp.isoformat(),
            "date": timestamp.strftime("%Y-%m-%d"),
            "time": timestamp.strftime("%H:%M:%S")
        }
        
        self.history.append(entry)
    
    def save_history(self) -> bool:
        """
        Save history to file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving history: {str(e)}")
            return False
    
    def load_history(self) -> bool:
        """
        Load history from file
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    self.history = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"Error loading history: {str(e)}")
            return False
    
    def get_emotion_counts(self) -> Dict[str, int]:
        """
        Get count of each emotion
        
        Returns:
            dict: Emotion counts
        """
        counts = {}
        for entry in self.history:
            emotion = entry["emotion"]
            counts[emotion] = counts.get(emotion, 0) + 1
        return counts
    
    def get_most_common_emotion(self) -> Optional[str]:
        """
        Get the most frequently detected emotion
        
        Returns:
            str: Most common emotion or None
        """
        counts = self.get_emotion_counts()
        if not counts:
            return None
        return max(counts, key=counts.get)
    
    def get_recent_emotions(self, count: int = 10) -> List[Dict]:
        """
        Get recent emotion detections
        
        Args:
            count: Number of recent emotions to return
            
        Returns:
            list: Recent emotion entries
        """
        return self.history[-count:] if self.history else []
    
    def get_emotions_by_date(self, date: str) -> List[Dict]:
        """
        Get emotions detected on a specific date
        
        Args:
            date: Date in YYYY-MM-DD format
            
        Returns:
            list: Emotion entries for that date
        """
        return [entry for entry in self.history if entry["date"] == date]
    
    def get_emotion_trend(self, days: int = 7) -> Dict[str, List[int]]:
        """
        Get emotion trend over recent days
        
        Args:
            days: Number of days to include
            
        Returns:
            dict: Emotion counts per day
        """
        from collections import defaultdict
        from datetime import timedelta
        
        today = datetime.now().date()
        trend = defaultdict(lambda: [0] * days)
        
        for entry in self.history:
            entry_date = datetime.fromisoformat(entry["timestamp"]).date()
            day_diff = (today - entry_date).days
            
            if 0 <= day_diff < days:
                emotion = entry["emotion"]
                trend[emotion][days - 1 - day_diff] += 1
        
        return dict(trend)
    
    def export_to_csv(self, filename: str = "emotion_history.csv") -> bool:
        """
        Export history to CSV file
        
        Args:
            filename: Output CSV filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.history:
                return False
            
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.history[0].keys())
                writer.writeheader()
                writer.writerows(self.history)
            
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
    
    def get_statistics(self) -> Dict:
        """
        Get comprehensive statistics
        
        Returns:
            dict: Statistics summary
        """
        if not self.history:
            return {
                "total_detections": 0,
                "emotion_counts": {},
                "most_common": None,
                "average_confidence": 0.0,
                "first_detection": None,
                "last_detection": None
            }
        
        counts = self.get_emotion_counts()
        confidences = [e.get("confidence", 0) for e in self.history]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return {
            "total_detections": len(self.history),
            "emotion_counts": counts,
            "most_common": self.get_most_common_emotion(),
            "average_confidence": avg_confidence,
            "first_detection": self.history[0]["timestamp"] if self.history else None,
            "last_detection": self.history[-1]["timestamp"] if self.history else None,
            "unique_emotions": len(counts)
        }
    
    def clear_history(self) -> None:
        """Clear all history"""
        self.history = []
        self.save_history()
    
    def get_emotion_duration(self) -> Dict[str, float]:
        """
        Calculate average duration between detections for each emotion
        
        Returns:
            dict: Average duration in seconds for each emotion
        """
        from collections import defaultdict
        
        emotion_times = defaultdict(list)
        
        for entry in self.history:
            emotion = entry["emotion"]
            timestamp = datetime.fromisoformat(entry["timestamp"])
            emotion_times[emotion].append(timestamp)
        
        durations = {}
        for emotion, times in emotion_times.items():
            if len(times) > 1:
                times.sort()
                diffs = [(times[i+1] - times[i]).total_seconds() 
                        for i in range(len(times) - 1)]
                durations[emotion] = sum(diffs) / len(diffs)
            else:
                durations[emotion] = 0.0
        
        return durations
    
    def __len__(self) -> int:
        """Return number of entries in history"""
        return len(self.history)
    
    def __str__(self) -> str:
        """String representation"""
        stats = self.get_statistics()
        return f"EmotionHistoryTracker(entries={stats['total_detections']}, most_common={stats['most_common']})"


# Example usage
if __name__ == "__main__":
    # Create tracker
    tracker = EmotionHistoryTracker()
    
    # Add some emotions
    tracker.add_emotion("Happy", confidence=0.95)
    tracker.add_emotion("Neutral", confidence=0.87)
    tracker.add_emotion("Happy", confidence=0.92)
    tracker.add_emotion("Sad", confidence=0.78)
    
    # Save history
    tracker.save_history()
    
    # Get statistics
    stats = tracker.get_statistics()
    print("Statistics:", json.dumps(stats, indent=2))
    
    # Export to CSV
    tracker.export_to_csv()
    
    print(f"\nTracker: {tracker}")
    print(f"Most common emotion: {tracker.get_most_common_emotion()}")
    print(f"Emotion counts: {tracker.get_emotion_counts()}")
