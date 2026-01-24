import time
from collections import deque

class MoodAnalytics:
    def __init__(self, window_size=15):
        self.emotion_window = deque(maxlen=window_size)
        self.start_time = time.time()
        self.energy_scores = {
            'Happy': 1.0, 'Surprise': 0.8, 'Neutral': 0.5, 
            'Sad': 0.2, 'Angry': 0.1, 'Fear': 0.1, 'Disgust': 0.0
        }

    def add_data(self, emotion):
        self.emotion_window.append(emotion)

    def get_trend(self):
        if len(self.emotion_window) < 5:
            return "Analyzing..."
        
        past = [self.energy_scores.get(e, 0.5) for e in list(self.emotion_window)[:5]]
        recent = [self.energy_scores.get(e, 0.5) for e in list(self.emotion_window)[-5:]]
        
        avg_past = sum(past) / len(past)
        avg_recent = sum(recent) / len(recent)
        
        if avg_recent > avg_past + 0.05: return "Improving 📈"
        if avg_recent < avg_past - 0.05: return "Declining 📉"
        return "Steady ↔️"

    def get_energy_level(self):
        """Calculates current energy percentage (0-100)."""
        if not self.emotion_window: return 50
        avg = sum(self.energy_scores.get(e, 0.5) for e in self.emotion_window) / len(self.emotion_window)
        return int(avg * 100)