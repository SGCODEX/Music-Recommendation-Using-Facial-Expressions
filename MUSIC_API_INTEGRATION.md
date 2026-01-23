# 🎵 Music API Integration Documentation

This document provides technical details about the Spotify and YouTube Music API integration in the Music Recommendation Using Facial Expressions project.

---

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Structure](#module-structure)
3. [Emotion Mapping System](#emotion-mapping-system)
4. [Spotify Integration](#spotify-integration)
5. [YouTube Integration](#youtube-integration)
6. [Usage Examples](#usage-examples)
7. [Error Handling & Fallbacks](#error-handling--fallbacks)
8. [API Limits & Best Practices](#api-limits--best-practices)
9. [Extending the System](#extending-the-system)

---

## 🏗 Architecture Overview

The music API integration is built with a modular architecture consisting of three main components:

```
code/music_apis/
├── __init__.py           # Module initialization
├── emotion_mapper.py     # Emotion → Music mapping logic
├── spotify_api.py        # Spotify Web API client
└── youtube_api.py        # YouTube Data API client
```

### Design Principles

- **Modularity**: Each API has its own isolated client class
- **Fallback Support**: Works gracefully without API credentials
- **Emotion-Centric**: All recommendations driven by detected emotions
- **Extensibility**: Easy to add new music platforms

---

## 📦 Module Structure

### `emotion_mapper.py`

Maps detected facial emotions to music characteristics.

**Key Features:**

- Predefined genre mappings for each emotion
- Audio feature targets (valence, energy, danceability, etc.)
- Search query generation for YouTube
- Mood descriptions

**Supported Emotions:**

- Happy
- Sad
- Angry
- Fear
- Surprise
- Disgust
- Neutral

### `spotify_api.py`

Client for Spotify Web API using OAuth Client Credentials flow.

**Key Methods:**

- `authenticate()`: Get access token
- `get_recommendations()`: Fetch tracks based on emotion parameters
- `search_tracks()`: Search for specific tracks
- `get_playlist_by_mood()`: Find mood-based playlists

### `youtube_api.py`

Client for YouTube Data API v3 with fallback web scraping.

**Key Methods:**

- `search_videos()`: Search for music videos
- `search_by_emotion()`: Emotion-specific video search
- `get_video_details()`: Retrieve video metadata
- `_fallback_search()`: Web scraping when API unavailable

---

## 🎭 Emotion Mapping System

The emotion mapper translates detected emotions into music characteristics that streaming APIs can understand.

### Spotify Audio Features

Each emotion maps to specific Spotify audio features:

```python
{
    'Happy': {
        'target_valence': 0.8,      # Positivity/happiness (0-1)
        'target_energy': 0.7,        # Intensity (0-1)
        'target_danceability': 0.7,  # Danceability (0-1)
        'genres': ['pop', 'dance', 'party']
    }
}
```

**Audio Feature Definitions:**

- **Valence**: Musical positivity (0 = sad, 1 = happy)
- **Energy**: Perceptual intensity (0 = calm, 1 = energetic)
- **Danceability**: Suitability for dancing (0-1)
- **Acousticness**: Presence of acoustic instruments (0-1)
- **Instrumentalness**: Lack of vocals (0-1)

### Complete Emotion Mapping

| Emotion      | Genres                 | Valence | Energy | Key Characteristics       |
| ------------ | ---------------------- | ------- | ------ | ------------------------- |
| **Happy**    | Pop, Dance, Party      | 0.8     | 0.7    | High energy, upbeat       |
| **Sad**      | Acoustic, Indie, Sad   | 0.2     | 0.3    | Low energy, melancholic   |
| **Angry**    | Metal, Rock, Hard Rock | 0.3     | 0.9    | Very high energy, intense |
| **Fear**     | Ambient, Chill, Lo-fi  | 0.3     | 0.4    | Calming, peaceful         |
| **Surprise** | Electronic, EDM        | 0.6     | 0.75   | Exciting, unexpected      |
| **Disgust**  | Alternative, Grunge    | 0.35    | 0.6    | Edgy, dark                |
| **Neutral**  | Indie, Folk            | 0.5     | 0.5    | Balanced, relaxed         |

### YouTube Query Mapping

Each emotion has multiple search queries for variety:

```python
'Happy': [
    'happy upbeat music',
    'feel good songs',
    'party playlist',
    'uplifting music'
]
```

---

## 🎵 Spotify Integration

### Authentication

Uses **OAuth Client Credentials** flow (no user login required):

1. Encode Client ID and Secret in Base64
2. Request access token from Spotify
3. Token valid for 1 hour (auto-refresh implemented)

**Code Example:**

```python
from music_apis import SpotifyMusicAPI

spotify = SpotifyMusicAPI(
    client_id='your_client_id',
    client_secret='your_client_secret'
)

# Authentication happens automatically on first API call
if spotify.authenticate():
    print("✅ Connected to Spotify")
```

### Getting Recommendations

The recommendation system uses Spotify's intelligent algorithm:

```python
from music_apis import EmotionMapper, SpotifyMusicAPI

mapper = EmotionMapper()
spotify = SpotifyMusicAPI(client_id, client_secret)

# Get emotion-based parameters
emotion = "Happy"
params = mapper.get_spotify_params(emotion)

# Fetch recommendations
tracks = spotify.get_recommendations(params, limit=10)

for track in tracks:
    print(f"{track['name']} by {track['artist']}")
    print(f"Preview: {track['preview_url']}")
    print(f"Spotify: {track['spotify_url']}")
```

### Track Information

Each track object contains:

```python
{
    'name': 'Song Title',
    'artist': 'Artist Name(s)',
    'album': 'Album Name',
    'album_art': 'https://...image.jpg',
    'preview_url': 'https://...preview.mp3',  # 30-second preview
    'spotify_url': 'https://open.spotify.com/track/...',
    'duration_ms': 240000,  # Duration in milliseconds
    'uri': 'spotify:track:...'  # Spotify URI
}
```

### API Endpoints Used

- `POST /api/token` - Authentication
- `GET /v1/recommendations` - Get recommendations
- `GET /v1/search` - Search tracks/playlists

---

## 📹 YouTube Integration

### With API Key

Uses YouTube Data API v3 for precise searches:

```python
from music_apis import YouTubeMusicAPI

youtube = YouTubeMusicAPI(api_key='your_api_key')
videos = youtube.search_by_emotion('Happy', max_results=10)

for video in videos:
    print(f"{video['title']} - {video['channel']}")
    print(f"Watch: {video['video_url']}")
```

### Fallback Method (No API Key)

When API key is unavailable, uses web scraping:

1. Constructs YouTube search URL
2. Fetches HTML content
3. Extracts video IDs using regex
4. Returns video information

**Note:** Fallback is less reliable and may break if YouTube changes their HTML structure.

### Video Information

Each video object contains:

```python
{
    'video_id': 'dQw4w9WgXcQ',
    'title': 'Video Title',
    'description': 'Video description...',
    'channel': 'Channel Name',
    'thumbnail': 'https://img.youtube.com/vi/.../hqdefault.jpg',
    'published_at': '2023-01-01T00:00:00Z',
    'video_url': 'https://www.youtube.com/watch?v=...',
    'embed_url': 'https://www.youtube.com/embed/...'
}
```

### API Endpoints Used

- `GET /youtube/v3/search` - Search videos
- `GET /youtube/v3/videos` - Get video details

---

## 💻 Usage Examples

### Basic Integration in Streamlit

```python
import streamlit as st
from music_apis import EmotionMapper, SpotifyMusicAPI, YouTubeMusicAPI

# Initialize
mapper = EmotionMapper()
spotify = SpotifyMusicAPI(client_id, client_secret)
youtube = YouTubeMusicAPI(api_key)

# Detect emotion (from your emotion detection model)
detected_emotion = "Happy"

# Get recommendations
st.write(f"## Music for your {detected_emotion} mood")

# Spotify
spotify_tracks = spotify.get_recommendations(
    mapper.get_spotify_params(detected_emotion),
    limit=10
)

for track in spotify_tracks:
    st.write(f"**{track['name']}** by {track['artist']}")
    if track['preview_url']:
        st.audio(track['preview_url'])
    st.write(f"[Open in Spotify]({track['spotify_url']})")

# YouTube
youtube_videos = youtube.search_by_emotion(detected_emotion, max_results=5)

for video in youtube_videos:
    st.write(f"**{video['title']}**")
    st.video(video['video_url'])
```

### Custom Emotion Mapping

You can customize emotion mappings:

```python
from music_apis import EmotionMapper

mapper = EmotionMapper()

# Modify existing mapping
mapper.emotion_to_spotify_params['Happy']['genres'] = ['jazz', 'swing', 'blues']
mapper.emotion_to_spotify_params['Happy']['target_valence'] = 0.9

# Get updated parameters
params = mapper.get_spotify_params('Happy')
```

### Playlist-Based Recommendations

```python
# Get mood-based playlists instead of tracks
playlists = spotify.get_playlist_by_mood('chill', limit=3)

for playlist in playlists:
    st.write(f"**{playlist['name']}**")
    st.write(f"By {playlist['owner']} • {playlist['tracks_total']} tracks")
    st.write(f"[Open Playlist]({playlist['playlist_url']})")
```

---

## 🛡️ Error Handling & Fallbacks

### Spotify Fallbacks

1. **No Credentials**: Shows warning, search disabled
2. **Authentication Failed**: Logs error, retries
3. **API Error**: Falls back to search instead of recommendations
4. **Rate Limit**: Waits and retries (exponential backoff)

### YouTube Fallbacks

1. **No API Key**: Automatically uses web scraping
2. **Quota Exceeded**: Uses fallback search method
3. **API Error**: Falls back to web scraping
4. **No Results**: Returns empty list gracefully

### Implementation Example

```python
try:
    tracks = spotify.get_recommendations(params, limit=10)
    if not tracks:
        # Fallback to search
        tracks = spotify.search_tracks(mood_description, limit=10)
except Exception as e:
    logger.error(f"Spotify error: {e}")
    st.warning("Using YouTube recommendations only")
```

---

## 📊 API Limits & Best Practices

### Spotify Rate Limits

- **Rate**: ~100 requests/second
- **Cost**: Free
- **Best Practice**:
  - Cache results for repeated requests
  - Implement exponential backoff on errors
  - Don't exceed 50 recommendations per call

### YouTube Rate Limits

- **Daily Quota**: 10,000 units (free tier)
- **Search Cost**: 100 units per request
- **Video Details**: 1 unit per request
- **Best Practice**:
  - Use `maxResults` parameter wisely (5-10 recommended)
  - Cache popular search results
  - Consider pagination for large result sets
  - Enable billing for production (50,000+ units/day)

### Optimization Tips

1. **Caching**: Use `st.cache_data` in Streamlit

   ```python
   @st.cache_data(ttl=3600)
   def get_cached_recommendations(emotion):
       return spotify.get_recommendations(params)
   ```

2. **Batch Requests**: Combine multiple operations
3. **Async Operations**: Use `asyncio` for concurrent API calls
4. **Connection Pooling**: Reuse HTTP connections

---

## 🔧 Extending the System

### Adding a New Music Platform

1. **Create API Client** (`code/music_apis/new_platform_api.py`):

   ```python
   class NewPlatformAPI:
       def __init__(self, api_key):
           self.api_key = api_key

       def search_music(self, emotion, limit=10):
           # Implementation
           pass
   ```

2. **Update Emotion Mapper**:

   ```python
   self.emotion_to_new_platform = {
       'Happy': {'query': 'upbeat music', 'filters': {...}},
       # ... other emotions
   }
   ```

3. **Integrate in UI**:
   ```python
   new_platform = NewPlatformAPI(api_key)
   results = new_platform.search_music(emotion)
   ```

### Adding New Emotions

1. **Update Emotion Mapper**:

   ```python
   self.emotion_to_spotify_params['Excited'] = {
       'genres': ['electronic', 'dance'],
       'target_valence': 0.85,
       'target_energy': 0.9,
       # ... other parameters
   }
   ```

2. **Update Model**: Retrain emotion detection model to recognize new emotion

### Custom Audio Features

Create specialized recommendations:

```python
# For workout music
workout_params = {
    'genres': ['workout', 'power'],
    'target_energy': 0.95,
    'target_tempo': 140,  # BPM
    'min_popularity': 60
}

tracks = spotify.get_recommendations(workout_params, limit=20)
```

---

## 📚 Additional Resources

- [Spotify Web API Reference](https://developer.spotify.com/documentation/web-api/reference/)
- [YouTube Data API Reference](https://developers.google.com/youtube/v3/docs)
- [Audio Features Explained](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)
- [OAuth 2.0 Client Credentials](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/)

---

## 🐛 Troubleshooting

### Common Issues

**"Spotify authentication failed"**

- Check Client ID and Secret
- Verify credentials have no extra spaces
- Check internet connection

**"YouTube quota exceeded"**

- Wait until midnight Pacific Time for reset
- Use fallback method (remove API key)
- Enable billing in Google Cloud

**"No recommendations found"**

- Try different emotion
- Check API credentials
- Verify internet connection
- Check console logs for detailed errors

**"Module not found: music_apis"**

- Ensure you're running from project root
- Check Python path includes `code/` directory

---

For more help, visit the [project repository](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions) or open an issue!
