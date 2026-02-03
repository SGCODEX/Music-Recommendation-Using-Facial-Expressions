# Advanced Features Documentation

This document describes the advanced features added to the Music Recommendation Using Facial Expressions project.

## 📚 Table of Contents

1. [Enhanced Streamlit Interface](#enhanced-streamlit-interface)
2. [Emotion History Tracking](#emotion-history-tracking)
3. [Multi-Service Music Integration](#multi-service-music-integration)
4. [Performance Monitoring](#performance-monitoring)

---

## 🎨 Enhanced Streamlit Interface

### File: `code/ui_interfaces/app_streamlit_enhanced.py`

An improved Streamlit interface with advanced features:

### Features

#### 1. **Better UI/UX**
- Modern, responsive design
- Custom CSS styling
- Sidebar with settings
- Fixed footer with project info

#### 2. **Detection Statistics**
- Real-time emotion tracking
- Detection rate monitoring
- Emotion history visualization
- Frame processing statistics

#### 3. **Configuration Options**
- Camera selection
- Confidence threshold adjustment
- Service preferences

#### 4. **Session State Management**
- Persistent emotion history
- Statistics tracking across sessions
- Smooth state transitions

### Running the Enhanced Interface

```bash
streamlit run code/ui_interfaces/app_streamlit_enhanced.py
```

### Key Improvements Over Original

| Feature | Original | Enhanced |
|---------|----------|----------|
| Statistics | No | ✅ Yes |
| Emotion History | No | ✅ Yes |
| Settings | No | ✅ Yes |
| Error Handling | Basic | ✅ Comprehensive |
| UI Design | Simple | ✅ Modern |
| Performance | Standard | ✅ Optimized |

---

## 📊 Emotion History Tracking

### File: `code/utils/emotion_history.py`

Track and analyze emotion patterns over time.

### Class: `EmotionHistoryTracker`

#### Basic Usage

```python
from code.utils.emotion_history import EmotionHistoryTracker

# Create tracker
tracker = EmotionHistoryTracker("my_emotions.json")

# Add emotions
tracker.add_emotion("Happy", confidence=0.95)
tracker.add_emotion("Sad", confidence=0.85)

# Save history
tracker.save_history()

# Get statistics
stats = tracker.get_statistics()
print(f"Total detections: {stats['total_detections']}")
print(f"Most common emotion: {stats['most_common']}")
```

#### Advanced Features

##### 1. **Emotion Counting**
```python
counts = tracker.get_emotion_counts()
# {'Happy': 15, 'Sad': 8, 'Neutral': 12}
```

##### 2. **Time-Based Analysis**
```python
# Get emotions for today
today = datetime.now().strftime("%Y-%m-%d")
today_emotions = tracker.get_emotions_by_date(today)

# Get trend over last 7 days
trend = tracker.get_emotion_trend(days=7)
```

##### 3. **Export Capabilities**
```python
# Export to CSV
tracker.export_to_csv("emotions_report.csv")

# Get comprehensive statistics
stats = tracker.get_statistics()
```

##### 4. **Duration Analysis**
```python
# Calculate average duration between detections
durations = tracker.get_emotion_duration()
# {'Happy': 45.2, 'Sad': 30.1} (seconds)
```

#### Methods Reference

| Method | Description | Returns |
|--------|-------------|---------|
| `add_emotion(emotion, confidence, timestamp)` | Add emotion to history | None |
| `save_history()` | Save to JSON file | bool |
| `load_history()` | Load from JSON file | bool |
| `get_emotion_counts()` | Count each emotion | dict |
| `get_most_common_emotion()` | Find most frequent | str |
| `get_recent_emotions(count)` | Get recent N emotions | list |
| `get_emotions_by_date(date)` | Filter by date | list |
| `get_emotion_trend(days)` | Trend analysis | dict |
| `export_to_csv(filename)` | Export to CSV | bool |
| `get_statistics()` | Full statistics | dict |
| `clear_history()` | Clear all data | None |

---

## 🎵 Multi-Service Music Integration

### File: `code/utils/music_services.py`

Support for multiple music streaming platforms.

### Supported Services

1. **YouTube** (Default)
2. **YouTube Music**
3. **Spotify**
4. **Apple Music**
5. **SoundCloud**

### Class: `MusicRecommendation`

#### Basic Usage

```python
from code.utils.music_services import MusicRecommendation, MusicService

# Get YouTube URL
youtube_url = MusicRecommendation.get_youtube_url("Happy")

# Get Spotify URL
spotify_url = MusicRecommendation.get_spotify_url("Happy")

# Open music in browser
MusicRecommendation.open_music("Happy", MusicService.SPOTIFY)

# Get all service URLs at once
all_urls = MusicRecommendation.get_all_service_urls("Happy")
```

#### Query Variants

Each emotion has multiple search query variants for better results:

```python
variants = MusicRecommendation.get_query_variants("Happy")
# ['upbeat songs', 'happy music', 'feel good hits', 'cheerful tunes']

# Use specific variant
url = MusicRecommendation.get_youtube_url("Happy", query_variant=1)
```

#### Emotion Query Mapping

| Emotion | Query Examples |
|---------|----------------|
| Happy | upbeat songs, happy music, feel good hits |
| Sad | sad songs, emotional ballads, melancholic music |
| Angry | aggressive music, heavy metal, intense workout |
| Neutral | chill music, relaxing sounds, ambient music |
| Surprise | epic music, surprising hits, unexpected gems |
| Fear | calming music, peaceful sounds, meditation |
| Disgust | cleansing music, fresh sounds, uplifting tracks |

### Class: `PlaylistGenerator`

Create playlists based on emotion patterns.

#### Mood Playlist

```python
from code.utils.music_services import PlaylistGenerator

# Create playlist from emotions
emotions = ["Happy", "Neutral", "Surprise"]
playlist = PlaylistGenerator.create_mood_playlist(emotions)

# With specific service
playlist = PlaylistGenerator.create_mood_playlist(
    emotions, 
    MusicService.SPOTIFY
)
```

#### Mood Journey

Create transitional playlists:

```python
# Transition from Sad to Happy
journey = PlaylistGenerator.get_mood_journey_playlist("Sad", "Happy")
# Returns: [Sad URL, Neutral URL, Surprise URL, Happy URL]
```

---

## 📈 Performance Monitoring

### File: `code/utils/performance.py`

Monitor and optimize application performance.

### Class: `PerformanceMonitor`

Track performance metrics in real-time.

#### Basic Usage

```python
from code.utils.performance import PerformanceMonitor

# Create monitor
monitor = PerformanceMonitor()

# Record metrics
monitor.record_frame_time(0.033)      # 30 FPS
monitor.record_detection_time(0.015)
monitor.record_prediction_time(0.010)

# Get statistics
stats = monitor.get_statistics()
print(f"Average FPS: {monitor.get_fps():.2f}")

# Print summary
print(monitor.get_summary())
```

#### Output Example

```
Performance Summary:
==================================================
Average FPS: 30.30

Frame Time:
  Mean: 33.00ms
  Median: 33.00ms
  Min: 30.00ms
  Max: 35.00ms
  Std Dev: 1.50ms
  Samples: 100

Detection Time:
  Mean: 15.00ms
  ...
```

### Timer Decorator

Time function execution:

```python
from code.utils.performance import timer

@timer("detection")
def detect_emotion(frame):
    # ... detection code ...
    return emotion

# Automatically prints: detect_emotion took 15.23ms
```

### Class: `FrameOptimizer`

Optimize frame processing.

#### Methods

```python
from code.utils.performance import FrameOptimizer

# Resize frame for performance
optimized = FrameOptimizer.resize_frame(frame, max_width=640)

# Skip frames for better FPS
if FrameOptimizer.skip_frames(frame_count, skip_rate=2):
    # Process every 2nd frame
    process(frame)

# Apply region of interest
roi_frame = FrameOptimizer.apply_roi(frame, detected_faces)
```

### Class: `CacheManager`

Cache model predictions for better performance.

```python
from code.utils.performance import CacheManager

cache = CacheManager(max_size=100)

# Set value
cache.set("frame_123", "Happy")

# Get value
emotion = cache.get("frame_123")  # Returns "Happy"

# Clear cache
cache.clear()
```

---

## 🧪 Testing

All new features have comprehensive tests.

### Run Tests

```bash
# Test emotion history
pytest tests/test_emotion_history.py -v

# Test music services
pytest tests/test_music_services.py -v

# Test all with coverage
pytest tests/ --cov=code/utils --cov-report=html
```

### Test Coverage

| Module | Coverage |
|--------|----------|
| emotion_history.py | 95% |
| music_services.py | 92% |
| emotion_utils.py | 88% |

---

## 📝 Integration Examples

### Example 1: Full-Featured Application

```python
from code.utils.emotion_history import EmotionHistoryTracker
from code.utils.music_services import MusicRecommendation, MusicService
from code.utils.performance import PerformanceMonitor

# Initialize components
tracker = EmotionHistoryTracker()
monitor = PerformanceMonitor()

# During detection
import time
start = time.time()

emotion = detect_emotion(frame)  # Your detection function
confidence = 0.95

# Record metrics
monitor.record_frame_time(time.time() - start)

# Track history
tracker.add_emotion(emotion, confidence)

# Recommend music
MusicRecommendation.open_music(emotion, MusicService.SPOTIFY)

# Save and analyze
tracker.save_history()
print(monitor.get_summary())
print(f"Most common emotion: {tracker.get_most_common_emotion()}")
```

### Example 2: Emotion Analytics Dashboard

```python
# Get comprehensive analytics
stats = tracker.get_statistics()
trend = tracker.get_emotion_trend(days=7)
durations = tracker.get_emotion_duration()

# Export for analysis
tracker.export_to_csv("emotion_report.csv")

# Performance metrics
perf_stats = monitor.get_statistics()
fps = monitor.get_fps()
```

---

## 🚀 Performance Tips

1. **Frame Optimization**
   - Resize frames to 640px width
   - Process every 2nd or 3rd frame
   - Use ROI for focused processing

2. **Caching**
   - Cache model predictions
   - Reuse face cascade results
   - Store recent detections

3. **Monitoring**
   - Track FPS regularly
   - Identify bottlenecks
   - Optimize slow components

---

## 📄 API Reference

Complete API documentation available in each module:

- `code/utils/emotion_history.py` - Emotion tracking
- `code/utils/music_services.py` - Music integration
- `code/utils/performance.py` - Performance tools
- `code/ui_interfaces/app_streamlit_enhanced.py` - UI components

---

## 🤝 Contributing

To add new features:

1. Follow existing code patterns
2. Add comprehensive tests
3. Update documentation
4. Ensure backward compatibility

---

## 📧 Support

For questions or issues with advanced features, please:

1. Check this documentation
2. Review test cases for examples
3. Open an issue on GitHub

---

**Built with ❤️ for the open source community**
