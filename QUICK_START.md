# 🎵 Music API Integration - Quick Start Guide

Welcome! This guide will help you get the new music streaming features up and running in minutes.

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

New packages installed:

- `spotipy` - Spotify API wrapper
- `google-api-python-client` - YouTube API client
- `python-dotenv` - Environment variable management

### Step 2: Get API Credentials (Optional)

The app works without credentials, but for the full experience:

**Option A: Set up Spotify (Recommended)**

1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Copy Client ID and Client Secret

**Option B: Set up YouTube**

1. Visit [Google Cloud Console](https://console.cloud.google.com/)
2. Enable YouTube Data API v3
3. Create an API key

**Option C: Set up Both** (Best experience!)

### Step 3: Configure Credentials

**Method 1: Using .env file (Recommended)**

```bash
cp .env.example .env
# Edit .env and add your credentials
```

**Method 2: Environment Variables**

```bash
export SPOTIFY_CLIENT_ID="your_id"
export SPOTIFY_CLIENT_SECRET="your_secret"
export YOUTUBE_API_KEY="your_key"
```

**Method 3: In-App** (Easiest)

- Run the app
- Go to Settings sidebar
- Enter credentials directly

### Step 4: Run the App

```bash
streamlit run code/deployment/app_with_music_apis.py
```

🎉 That's it! You're ready to go!

---

## 🎮 How to Use

1. **Allow Camera Access** when prompted by your browser
2. **Look at the camera** for a few seconds
3. **Click "Get Music Recommendations"**
4. **Enjoy your personalized playlist!**

### Features You'll See:

**Spotify Tab:**

- 🎵 Real tracks with 30-second previews
- 🎨 Album artwork
- 👨‍🎤 Artist information
- 🔗 Direct links to Spotify

**YouTube Tab:**

- 📹 Music videos matching your mood
- ▶️ Play videos directly in the app
- 🎬 Thumbnails and channel info
- 🔗 Links to YouTube

---

## 📋 What's New?

### Before (v1.0)

- Opens YouTube search in browser
- Generic search results
- No real music playback
- Limited customization

### After (v2.0 with APIs) 🎉

- ✅ Real Spotify tracks with audio previews
- ✅ Curated YouTube music videos
- ✅ Direct playback in app
- ✅ Album art and metadata
- ✅ Emotion-specific recommendations
- ✅ Configurable settings
- ✅ Works with or without API keys

---

## 🔧 Troubleshooting

### "No Spotify tracks found"

- Check your credentials in Settings sidebar
- Try the YouTube tab instead
- The app will show helpful error messages

### "YouTube quota exceeded"

- Wait until midnight Pacific Time
- Or use the app without YouTube API key (fallback method works!)

### "Camera not working"

- Check browser permissions
- Make sure no other app is using the camera
- Try a different browser (Chrome recommended)

### "Module not found: music_apis"

- Make sure you're in the project root directory
- Run: `cd Music-Recommendation-Using-Facial-Expressions`

---

## 💡 Tips & Tricks

### Get Better Recommendations

- Make sure your face is well-lit
- Look directly at the camera
- Hold your expression for 2-3 seconds
- Try different emotions for variety!

### Customize Your Experience

- Adjust number of recommendations (5-20) in Settings
- Toggle Spotify/YouTube sources
- Enable auto-play for instant music

### Save Your Favorites

- Click "Open in Spotify" to add tracks to your playlists
- Save YouTube videos to your YouTube account
- Share recommendations with friends!

---

## 📚 Need More Help?

### Full Documentation

- [API Setup Guide](API_SETUP_GUIDE.md) - Detailed credential setup
- [Music API Integration](MUSIC_API_INTEGRATION.md) - Technical documentation
- [Main README](README.md) - Project overview

### Testing Your Setup

Run the test script to verify everything works:

```bash
python test_music_apis.py
```

### Example Commands

**Run enhanced app:**

```bash
streamlit run code/deployment/app_with_music_apis.py
```

**Run original app:**

```bash
streamlit run code/deployment/app.py
```

**Test APIs:**

```bash
python test_music_apis.py
```

---

## 🎯 What Each File Does

```
Music-Recommendation-Using-Facial-Expressions/
├── code/
│   ├── music_apis/              # 🆕 Music API integration
│   │   ├── emotion_mapper.py    # Maps emotions to music
│   │   ├── spotify_api.py       # Spotify client
│   │   └── youtube_api.py       # YouTube client
│   ├── deployment/
│   │   ├── app.py               # Original app
│   │   └── app_with_music_apis.py  # 🆕 Enhanced app
│   └── model/
│       └── fer2013_mini_XCEPTION.102-0.66.hdf5  # Emotion model
├── .env.example                 # 🆕 Credential template
├── API_SETUP_GUIDE.md          # 🆕 Setup instructions
├── MUSIC_API_INTEGRATION.md    # 🆕 Technical docs
├── test_music_apis.py          # 🆕 Test script
└── requirements.txt            # Updated dependencies
```

---

## 🌟 Pro Tips

### For Developers

```python
# Use the APIs in your own code
from music_apis import EmotionMapper, SpotifyMusicAPI, YouTubeMusicAPI

mapper = EmotionMapper()
spotify = SpotifyMusicAPI(client_id, client_secret)

# Get recommendations
params = mapper.get_spotify_params('Happy')
tracks = spotify.get_recommendations(params, limit=10)
```

### For Content Creators

- Record your emotion detection sessions
- Share playlists generated by the app
- Create mood-based compilation videos

### For Researchers

- Customize emotion-to-genre mappings
- Add new music platforms
- Experiment with different audio features

---

## 🎓 Learn More

### About the APIs

- [Spotify Web API Docs](https://developer.spotify.com/documentation/web-api)
- [YouTube Data API Docs](https://developers.google.com/youtube/v3)

### About the Technology

- Facial emotion recognition using deep learning
- Real-time video processing with OpenCV
- OAuth authentication flows
- RESTful API integration

---

## 🆘 Getting Help

### Having Issues?

1. Check the [Troubleshooting](#-troubleshooting) section above
2. Run `python test_music_apis.py` to diagnose
3. Check [GitHub Issues](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/issues)
4. Ask in the community

### Want to Contribute?

- See [CONTRIBUTING.md](CONTRIBUTING.md)
- All PRs should go to the `contribution` branch
- We welcome bug fixes, features, and documentation!

---

## ✨ Enjoy Your Music!

Now you have a complete emotion-aware music recommendation system powered by real streaming platforms. Have fun discovering new music based on your mood! 🎵🎉

**Star the repo** ⭐ if you find this useful!
