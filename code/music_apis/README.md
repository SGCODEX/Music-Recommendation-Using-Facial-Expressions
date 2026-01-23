# 🎵 Music APIs Module

This module provides intelligent music recommendations based on detected facial emotions using Spotify and YouTube APIs.

---

## 📦 Module Structure

```
music_apis/
├── __init__.py           # Module exports
├── emotion_mapper.py     # Emotion → Music mapping
├── spotify_api.py        # Spotify Web API client
└── youtube_api.py        # YouTube Data API client
```

---

## 🚀 Quick Start

```python
from music_apis import EmotionMapper, SpotifyMusicAPI, YouTubeMusicAPI

# Initialize components
mapper = EmotionMapper()
spotify = SpotifyMusicAPI(client_id='your_id', client_secret='your_secret')
youtube = YouTubeMusicAPI(api_key='your_key')

# Detect emotion (from your emotion detection system)
detected_emotion = "Happy"

# Get Spotify recommendations
params = mapper.get_spotify_params(detected_emotion)
tracks = spotify.get_recommendations(params, limit=10)

# Get YouTube videos
videos = youtube.search_by_emotion(detected_emotion, max_results=5)

# Use the results
for track in tracks:
    print(f"{track['name']} by {track['artist']}")

for video in videos:
    print(f"{video['title']} - {video['video_url']}")
```

---

## 📚 Components

### EmotionMapper

Maps detected emotions to music characteristics.

**Methods:**

- `get_spotify_params(emotion)` - Get Spotify recommendation parameters
- `get_youtube_query(emotion)` - Get YouTube search query
- `get_all_youtube_queries(emotion)` - Get all possible queries
- `get_mood_description(emotion)` - Get mood description

**Supported Emotions:**

- Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral

**Example:**

```python
mapper = EmotionMapper()
params = mapper.get_spotify_params('Happy')
# Returns: {'genres': ['pop', 'dance'], 'target_valence': 0.8, ...}
```

### SpotifyMusicAPI

Client for Spotify Web API.

**Methods:**

- `authenticate()` - OAuth authentication
- `get_recommendations(emotion_params, limit)` - Get track recommendations
- `search_tracks(query, limit)` - Search for tracks
- `get_playlist_by_mood(mood, limit)` - Find playlists

**Example:**

```python
spotify = SpotifyMusicAPI(client_id, client_secret)
tracks = spotify.get_recommendations(params, limit=10)

for track in tracks:
    print(track['name'])
    print(track['preview_url'])  # 30-second preview
    print(track['spotify_url'])  # Open in Spotify
```

### YouTubeMusicAPI

Client for YouTube Data API with fallback.

**Methods:**

- `search_videos(query, max_results)` - General search
- `search_by_emotion(emotion, max_results)` - Emotion-specific search
- `get_video_details(video_id)` - Get video metadata
- `_fallback_search(query, max_results)` - Web scraping fallback

**Example:**

```python
youtube = YouTubeMusicAPI(api_key)
videos = youtube.search_by_emotion('Happy', max_results=5)

for video in videos:
    print(video['title'])
    print(video['video_url'])
    print(video['thumbnail'])
```

---

## 🎭 Emotion Mapping

### Audio Features

Each emotion maps to specific Spotify audio features:

| Feature          | Description          | Range                    |
| ---------------- | -------------------- | ------------------------ |
| Valence          | Musical positivity   | 0 (sad) - 1 (happy)      |
| Energy           | Intensity            | 0 (calm) - 1 (energetic) |
| Danceability     | Dance suitability    | 0 - 1                    |
| Acousticness     | Acoustic instruments | 0 - 1                    |
| Instrumentalness | Lack of vocals       | 0 - 1                    |

### Emotion Examples

**Happy:**

```python
{
    'genres': ['pop', 'dance', 'party'],
    'target_valence': 0.8,
    'target_energy': 0.7,
    'target_danceability': 0.7
}
```

**Sad:**

```python
{
    'genres': ['acoustic', 'indie', 'sad'],
    'target_valence': 0.2,
    'target_energy': 0.3,
    'target_acousticness': 0.7
}
```

**Angry:**

```python
{
    'genres': ['metal', 'rock', 'hard-rock'],
    'target_valence': 0.3,
    'target_energy': 0.9
}
```

---

## 🔧 Advanced Usage

### Custom Emotion Mapping

```python
mapper = EmotionMapper()

# Modify existing mapping
mapper.emotion_to_spotify_params['Happy']['genres'] = ['jazz', 'swing']
mapper.emotion_to_spotify_params['Happy']['target_valence'] = 0.9

# Use custom params
params = mapper.get_spotify_params('Happy')
```

### Error Handling

```python
try:
    if spotify.authenticate():
        tracks = spotify.get_recommendations(params, limit=10)
        if not tracks:
            # Fallback to search
            tracks = spotify.search_tracks('happy music', limit=10)
except Exception as e:
    print(f"Spotify error: {e}")
    # Use YouTube instead
    videos = youtube.search_by_emotion('Happy')
```

### Caching (Streamlit)

```python
import streamlit as st

@st.cache_data(ttl=3600)
def get_cached_recommendations(emotion, client_id, client_secret):
    spotify = SpotifyMusicAPI(client_id, client_secret)
    mapper = EmotionMapper()
    params = mapper.get_spotify_params(emotion)
    return spotify.get_recommendations(params, limit=10)
```

---

## 📊 Return Formats

### Spotify Track Object

```python
{
    'name': 'Song Title',
    'artist': 'Artist Name(s)',
    'album': 'Album Name',
    'album_art': 'https://...image.jpg',
    'preview_url': 'https://...preview.mp3',  # 30-sec
    'spotify_url': 'https://open.spotify.com/track/...',
    'duration_ms': 240000,
    'uri': 'spotify:track:...'
}
```

### YouTube Video Object

```python
{
    'video_id': 'dQw4w9WgXcQ',
    'title': 'Video Title',
    'description': 'Description...',
    'channel': 'Channel Name',
    'thumbnail': 'https://img.youtube.com/vi/.../hqdefault.jpg',
    'published_at': '2023-01-01T00:00:00Z',
    'video_url': 'https://www.youtube.com/watch?v=...',
    'embed_url': 'https://www.youtube.com/embed/...'
}
```

---

## 🛡️ Error Handling

### Spotify

- **No credentials**: Returns empty list
- **Auth failed**: Logs error, returns empty list
- **API error**: Falls back to search
- **Rate limit**: Implements backoff

### YouTube

- **No API key**: Uses fallback web scraping
- **Quota exceeded**: Uses fallback
- **API error**: Uses fallback
- **No results**: Returns empty list

---

## 🔑 Environment Variables

```bash
# .env file
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
```

**Usage:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

spotify = SpotifyMusicAPI(
    os.getenv('SPOTIFY_CLIENT_ID'),
    os.getenv('SPOTIFY_CLIENT_SECRET')
)
```

---

## 📈 Best Practices

1. **Credential Management**
   - Use environment variables
   - Never hardcode API keys
   - Keep `.env` in `.gitignore`

2. **API Usage**
   - Cache results when possible
   - Implement rate limiting
   - Handle errors gracefully
   - Use fallback methods

3. **Performance**
   - Limit recommendation count
   - Reuse API clients
   - Batch operations
   - Implement timeouts

4. **User Experience**
   - Show loading states
   - Display error messages
   - Provide fallback options
   - Enable offline mode

---

## 🧪 Testing

```python
# Test emotion mapper
mapper = EmotionMapper()
assert 'genres' in mapper.get_spotify_params('Happy')

# Test Spotify
spotify = SpotifyMusicAPI(client_id, client_secret)
assert spotify.authenticate() == True

# Test YouTube
youtube = YouTubeMusicAPI(api_key)
videos = youtube.search_by_emotion('Happy')
assert len(videos) > 0
```

Run full test suite:

```bash
python test_music_apis.py
```

---

## 📚 Dependencies

```
requests>=2.31.0
spotipy>=2.23.0
google-api-python-client>=2.100.0
python-dotenv>=1.0.0
```

---

## 🔗 Resources

- [Spotify Web API Docs](https://developer.spotify.com/documentation/web-api)
- [YouTube Data API Docs](https://developers.google.com/youtube/v3)
- [Audio Features Guide](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)

---

## 🐛 Troubleshooting

**"Module not found: music_apis"**

```python
import sys
sys.path.append('path/to/code')
from music_apis import EmotionMapper
```

**"Authentication failed"**

- Check credentials are correct
- Verify no extra spaces
- Check internet connection

**"No recommendations"**

- Try different emotion
- Check API limits
- Use fallback methods

---

## 📄 License

This module is part of the Music-Recommendation-Using-Facial-Expressions project.
See LICENSE file in project root.

---

For more details, see:

- [API Setup Guide](../API_SETUP_GUIDE.md)
- [Music API Integration Docs](../MUSIC_API_INTEGRATION.md)
- [Quick Start Guide](../QUICK_START.md)
