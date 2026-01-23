## Music-Recommendation-Using-Facial-Expressions

Please give us a ⭐ and fork this repo to get started. Thank you 🙌🙌.

### Project Overview

This project is a Python-based application that uses OpenCV for real-time facial detection and a pre-trained deep learning model (fer2013_mini_XCEPTION.102-0.66.hdf5) to recognize and analyze facial expressions. By capturing live video feed from the user’s webcam, it identifies the user’s emotions—such as happiness, sadness, anger, or neutrality—based on facial cues.

Once the emotion is detected, the application constructs a YouTube search query tailored to the identified mood. Using the webbrowser module, the application automatically opens relevant YouTube search results in the user’s default browser, allowing them to access music that aligns with their current emotional state. The requests library further supports this functionality by enabling API interactions for a smoother YouTube search experience.

This project combines elements of computer vision and deep learning with web integration to create a personalized and interactive music recommendation system. It demonstrates the potential of AI-powered emotion detection in real-world applications, where user experience can be enhanced through real-time responsiveness and intelligent content recommendations.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git
    cd Music-Recommendation-Using-Facial-Expressions
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt --quiet
    ```
3.  **Setup API Credentials (Optional but Recommended):**
    ```bash
    cp .env.example .env
    # Edit .env and add your Spotify and YouTube API credentials
    ```
    See [API Setup Guide](API_SETUP_GUIDE.md) for detailed instructions on obtaining API keys.

### Quick Start

Get the application running in just 3 steps:

1. **Clone and setup:**

   ```bash
   git clone https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions.git
   cd Music-Recommendation-Using-Facial-Expressions
   pip install -r requirements.txt --quiet
   ```

2. **Choose your interface** and run one of these commands:
   - **🎵 Enhanced Streamlit App with Music APIs (RECOMMENDED):**
     ```bash
     streamlit run code/deployment/app_with_music_apis.py
     ```
     _Features real Spotify tracks, YouTube videos, audio previews, and album art!_
   - **Streamlit Web App (Basic):**
     ```bash
     streamlit run code/ui_interfaces/app_local_streamlit.py
     ```
   - **Desktop App:**
     ```bash
     python code/ui_interfaces/app_PySimpleGUI.py
     ```
   - **Terminal/CLI:**
     ```bash
     python code/ui_interfaces/cli_main.py
     ```

3. **Allow webcam access** when prompted and start detecting emotions! 🎵

> **Note:** Ensure your webcam is connected and working properly before running the application.

### How to Run & Interface Options

This project supports three ways to interact with the emotion-based music recommendation system:

**a)CLI Mode (Terminal)**

- Run the core logic directly via terminal (no GUI).
  `bash
python code\ui_interfaces\cli_main.py
`
  **b)Web Interface (Streamlit)**
- Clean, browser-based UI using Streamlit.
  `bash
streamlit run code\ui_interfaces\app_local_streamlit.py
`
  **c)Desktop App (PySimpleGUI)**
- Native desktop GUI that runs as a standalone application.
  `bash
python code\ui_interfaces\app_PySimpleGUI.py
`
  **Ignore - Deployed File**
  **Core Technologies:**
- **Python**: Primary programming language for its versatility and extensive libraries
- **OpenCV**: Real-time image and video processing, including facial detection
- **TensorFlow and Keras**: Deep learning model for facial expression recognition
- **fer2013_mini_XCEPTION.102-0.66.hdf5**: Pre-trained model for facial emotion recognition
- **Streamlit**: Modern web interface framework for interactive applications

**🆕 Music API Integration:**

- **Spotify Web API**: Access to millions of tracks with audio previews, album art, and metadata
- **YouTube Data API v3**: Music video search and recommendations
- **Emotion Mapping Engine**: Custom algorithm mapping emotions to music genres and moods
- **OAuth Authentication**: Secure API access management

**Supporting Libraries:**

- **requests**: HTTP requests for API interactions
- **python-dotenv**: Environment variable management for secure credential storage
- **google-api-python-client**: YouTube API integration
- **spotipy**: Simplified Spotify API wrapper

### How it Works / Usage

1.  **Facial Detection:**
    - The script captures a video feed from your webcam
    - OpenCV is used to detect faces in each frame
2.  **Emotion Recognition:**
    - Detected faces are processed by the trained model
    - The model predicts the dominant emotion (e.g., happy, sad, angry, neutral)
    - Script captures the emotion when we click on the screen, the clicked emotion is stored as current emotion
3.  **🎵 Smart Music Recommendation:**
    - Emotion is mapped to specific music characteristics (genres, moods, audio features)
    - **Spotify API** fetches real tracks with audio previews and metadata
    - **YouTube API** retrieves curated music videos
    - Results are displayed with playback options, album art, and links

- Watch & Contribute to Community Demo Videos here: [Demo Videos](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/contribution/code/new_models/demo.md)
- Example Demo Video: [Demo Video for CLI Interface](https://www.youtube.com/watch?v=Qj5yUBjSr7I)

### Main Features

- Employs a pre-trained deep learning model (fer2013_mini_XCEPTION.102-0.66.hdf5) to accurately identify facial expressions
- Recognizes a range of emotions: Happy, Sad, Angry, Fear, Surprise, Disgust, and Neutral
- Real-time emotion display with confidence visualization

**2. 🎵 Intelligent Music Recommendation System:**

- **Spotify Integration:**
  - Fetches real tracks based on emotion-specific audio features (valence, energy, danceability)
  - Provides 30-second audio previews for instant listening
  - Displays album artwork, artist information, and metadata
  - Direct links to open tracks in Spotify app/web

- **YouTube Integration:**
  - Curated music video recommendations based on detected emotion
  - Direct video playback within the application
  - Multiple video options with thumbnails and descriptions
  - Fallback search when API limits are reached

- **Smart Emotion Mapping:**
  - Custom algorithm maps emotions to specific music genres and moods
  - Happy → Pop, Dance, Party music
  - Sad → Acoustic, Indie, Emotional tracks
  - Angry → Metal, Rock, Intense music
  - Fear → Calming, Ambient, Peaceful sounds
  - And more...

**3. Intuitive User Interface:**

- Modern, responsive Streamlit web interface
- Side-by-side comparison of Spotify and YouTube recommendations
- Easy credential management through settings sidebar
- Auto-play options for seamless experience
- Beautiful gradient design with smooth animations

**4. Flexible Configuration:**

- Works with or without API credentials (uses fallback methods)
- Configurable number of recommendations (5-20 tracks)
- Toggle between Spotify and YouTube sources
- Environment variable support for production deployment

### 🔑 API Setup

To enable real music streaming features, you'll need API credentials from Spotify and YouTube:

1. **Spotify API**: Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) to create an app and get your credentials
2. **YouTube API**: Visit [Google Cloud Console](https://console.cloud.google.com/) to enable YouTube Data API v3 and get an API key

For detailed step-by-step instructions, see our [API Setup Guide](API_SETUP_GUIDE.md).

**Note:** The application works without credentials using fallback methods, but the full experience requires API keys.

### Customization & Additional Considerations

- **Model:** Experiment with different pre-trained models or fine-tune the existing one for more accurate emotion recognition
- **Music APIs:** Customize emotion-to-genre mappings in `code/music_apis/emotion_mapper.py`
- **User Interface:** Modify the Streamlit UI or create custom interfaces
- **Privacy:** Be mindful of privacy concerns when capturing and processing facial data
- **Performance:** Optimize the code for real-time performance, especially on resource-constrained devices
- **Error Handling:** Robust error handling is implemented with fallback methods
- **Additional APIs:** Consider integrating Apple Music, SoundCloud, or other streaming services

### Contribution

**NOTE: Please create PRs only to the contribution branch. All others will be automatically closed.**

We welcome contributions to this project. Feel free to fork the repository, make improvements, and submit pull requests.
We value all contributions, whether it's through code, documentation, creating demos or just spreading the word.
**If you have introduced a new Computer Vision Library based code or new model or using new library (such as fer), Please submit final code in new_models folder.**
Here are a few useful resources to help you get started:

- For contributions, [Check out the contribution guide](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/CONTRIBUTING.md) .

### PR Template

Please submit all PRs in this format: [PR Template](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/CONTRIBUTING.md#pr-template)

### License

This project is licensed under the [MIT License](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/blob/main/LICENSE)

### Contact Us

For any questions or issues, please contact us at shivampilot2004@gmail.com
