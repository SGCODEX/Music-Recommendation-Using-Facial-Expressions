# 🎵 How to Get API Credentials for Music Integration

This guide will help you set up Spotify and YouTube API credentials to enable real music recommendations in the application.

---

## 🎧 Spotify Web API Setup

### Step 1: Create a Spotify Developer Account

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account (or create one if you don't have it)
3. Accept the Terms of Service

### Step 2: Create an App

1. Click **"Create an App"**
2. Fill in the details:
   - **App Name**: Music Recommendation System (or any name)
   - **App Description**: Emotion-based music recommendation using facial recognition
   - **Redirect URI**: `http://localhost:8501` (for local testing)
3. Accept the terms and click **"Create"**

### Step 3: Get Your Credentials

1. In your app dashboard, you'll see:
   - **Client ID**: Copy this value
   - **Client Secret**: Click "Show Client Secret" and copy it
2. Save these credentials securely

### Step 4: Configure the Application

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your credentials:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

---

## 📹 YouTube Data API Setup

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Click **"Create Project"** and give it a name

### Step 2: Enable YouTube Data API

1. In the left menu, go to **"APIs & Services"** → **"Library"**
2. Search for **"YouTube Data API v3"**
3. Click on it and press **"Enable"**

### Step 3: Create API Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"Create Credentials"** → **"API Key"**
3. Copy the generated API key
4. (Optional) Restrict the API key:
   - Click on the API key name
   - Under "API restrictions", select "Restrict key"
   - Choose "YouTube Data API v3"
   - Save

### Step 4: Configure the Application

1. Add your YouTube API key to `.env`:
   ```
   YOUTUBE_API_KEY=your_api_key_here
   ```

---

## 🚀 Running the Application

### Option 1: Using Environment Variables (Recommended)

1. Make sure your `.env` file is configured with all credentials
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the enhanced app:
   ```bash
   streamlit run code/deployment/app_with_music_apis.py
   ```

### Option 2: Without API Credentials (Limited Functionality)

The application includes fallback methods:

- **Spotify**: Will show a warning; try the YouTube fallback
- **YouTube**: Uses web scraping as fallback (may be less reliable)

Simply run the app without credentials, and it will use fallback methods:

```bash
streamlit run code/deployment/app_with_music_apis.py
```

You can also enter credentials directly in the app's sidebar settings.

---

## 🔧 Troubleshooting

### Spotify Issues

- **"Authentication failed"**: Double-check your Client ID and Client Secret
- **"Invalid credentials"**: Make sure there are no extra spaces in your `.env` file
- **Rate limiting**: Spotify has rate limits; wait a few minutes and try again

### YouTube Issues

- **"Quota exceeded"**: YouTube API has daily quotas. You can:
  - Wait until the quota resets (midnight Pacific Time)
  - Enable billing in Google Cloud (increases quota)
  - Use the fallback method (no API key required)
- **"API key invalid"**: Verify the API key is correct and YouTube Data API v3 is enabled

### General Issues

- **Module not found**: Run `pip install -r requirements.txt`
- **Model not loading**: Make sure `fer2013_mini_XCEPTION.102-0.66.hdf5` is in `code/model/`
- **Camera not working**: Check browser permissions and try using HTTPS

---

## 📊 API Usage Limits

### Spotify

- **Client Credentials Flow**:
  - No user authentication required
  - Rate limit: ~100 requests per second
  - Free tier available

### YouTube

- **Free Tier**: 10,000 quota units per day
- Each search costs ~100 units
- ~100 searches per day possible
- Paid tier available for higher quotas

---

## 🔒 Security Best Practices

1. **Never commit `.env` file to git**
   - It's already in `.gitignore`
2. **Use environment variables in production**
3. **Restrict API keys** to specific domains/IPs in production
4. **Rotate credentials** regularly
5. **Monitor API usage** in respective dashboards

---

## 📚 Additional Resources

- [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
- [YouTube Data API Documentation](https://developers.google.com/youtube/v3)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## 💡 Tips

- **Testing**: Use a separate project for testing with lower quotas
- **Caching**: Consider implementing caching to reduce API calls
- **Alternatives**: Can integrate other services like Apple Music, SoundCloud, etc.
- **Offline Mode**: The app can work without APIs using the fallback methods

---

For more help, check the [project GitHub repository](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions) or create an issue!
