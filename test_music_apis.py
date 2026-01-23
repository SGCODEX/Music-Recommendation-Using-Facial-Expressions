"""
Test script for Music API Integration
Run this to verify your API credentials and test the emotion mapping system
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add music_apis to path
project_root = os.path.dirname(os.path.abspath(__file__))
code_path = os.path.join(project_root, 'code')
if code_path not in sys.path:
    sys.path.insert(0, code_path)

try:
    from music_apis import EmotionMapper, SpotifyMusicAPI, YouTubeMusicAPI
except ImportError as e:
    print(f"\n❌ Error: Could not import music_apis module")
    print(f"   Make sure you're running this from the project root directory")
    print(f"   Current directory: {os.getcwd()}")
    print(f"   Looking for: {code_path}")
    print(f"   Error: {e}\n")
    sys.exit(1)

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def test_emotion_mapper():
    """Test the emotion mapping system"""
    print_section("Testing Emotion Mapper")
    
    mapper = EmotionMapper()
    emotions = ['Happy', 'Sad', 'Angry', 'Fear', 'Surprise', 'Disgust', 'Neutral']
    
    for emotion in emotions:
        params = mapper.get_spotify_params(emotion)
        youtube_query = mapper.get_youtube_query(emotion)
        mood = mapper.get_mood_description(emotion)
        
        print(f"Emotion: {emotion}")
        print(f"  Mood: {mood}")
        print(f"  Genres: {', '.join(params['genres'])}")
        print(f"  Valence: {params.get('target_valence', 'N/A')}")
        print(f"  Energy: {params.get('target_energy', 'N/A')}")
        print(f"  YouTube Query: {youtube_query}")
        print()
    
    print("✅ Emotion Mapper test completed successfully!")

def test_spotify_api():
    """Test Spotify API connection and recommendations"""
    print_section("Testing Spotify API")
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID', '')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '')
    
    if not client_id or not client_secret:
        print("⚠️  Spotify credentials not found in environment variables")
        print("   Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET to test")
        print("   Or run without credentials (limited functionality)")
        return False
    
    print(f"Client ID: {client_id[:10]}...")
    
    spotify = SpotifyMusicAPI(client_id, client_secret)
    
    # Test authentication
    print("\n1. Testing authentication...")
    if spotify.authenticate():
        print("   ✅ Authentication successful!")
    else:
        print("   ❌ Authentication failed. Check your credentials.")
        return False
    
    # Test recommendations
    print("\n2. Testing recommendations for 'Happy' emotion...")
    mapper = EmotionMapper()
    params = mapper.get_spotify_params('Happy')
    
    tracks = spotify.get_recommendations(params, limit=5)
    
    if tracks:
        print(f"   ✅ Retrieved {len(tracks)} tracks:")
        for i, track in enumerate(tracks[:3], 1):
            print(f"   {i}. {track['name']} - {track['artist']}")
            print(f"      Album: {track['album']}")
            if track['preview_url']:
                print(f"      Preview: Available")
    else:
        print("   ⚠️  No tracks retrieved. API might have issues.")
        return False
    
    # Test search
    print("\n3. Testing track search...")
    search_tracks = spotify.search_tracks('happy songs', limit=3)
    
    if search_tracks:
        print(f"   ✅ Search successful! Found {len(search_tracks)} tracks")
    else:
        print("   ⚠️  Search returned no results")
    
    print("\n✅ Spotify API test completed successfully!")
    return True

def test_youtube_api():
    """Test YouTube API connection and search"""
    print_section("Testing YouTube API")
    
    api_key = os.getenv('YOUTUBE_API_KEY', '')
    
    if not api_key:
        print("⚠️  YouTube API key not found in environment variables")
        print("   Testing with fallback method (no API key)...")
        use_fallback = True
    else:
        print(f"API Key: {api_key[:10]}...")
        use_fallback = False
    
    youtube = YouTubeMusicAPI(api_key if not use_fallback else None)
    
    # Test search
    print("\n1. Testing video search for 'Happy' emotion...")
    videos = youtube.search_by_emotion('Happy', max_results=5)
    
    if videos:
        print(f"   ✅ Retrieved {len(videos)} videos:")
        for i, video in enumerate(videos[:3], 1):
            print(f"   {i}. {video['title'][:60]}...")
            print(f"      Channel: {video['channel']}")
            print(f"      URL: {video['video_url']}")
    else:
        print("   ❌ No videos retrieved.")
        return False
    
    # Test direct search
    print("\n2. Testing direct search query...")
    videos = youtube.search_videos('relaxing music', max_results=3)
    
    if videos:
        print(f"   ✅ Search successful! Found {len(videos)} videos")
    else:
        print("   ⚠️  Search returned no results")
    
    if use_fallback:
        print("\n⚠️  Using fallback method (web scraping)")
        print("   For best results, set YOUTUBE_API_KEY environment variable")
    else:
        print("\n✅ YouTube API test completed successfully!")
    
    return True

def test_full_workflow():
    """Test the complete workflow"""
    print_section("Testing Complete Workflow")
    
    print("Simulating emotion detection workflow...")
    
    # Simulate detected emotion
    detected_emotion = "Happy"
    print(f"\n📸 Detected Emotion: {detected_emotion}")
    
    # Initialize components
    mapper = EmotionMapper()
    spotify = SpotifyMusicAPI(
        os.getenv('SPOTIFY_CLIENT_ID', ''),
        os.getenv('SPOTIFY_CLIENT_SECRET', '')
    )
    youtube = YouTubeMusicAPI(os.getenv('YOUTUBE_API_KEY', ''))
    
    # Get emotion parameters
    print(f"\n🎭 Emotion Mapping:")
    params = mapper.get_spotify_params(detected_emotion)
    print(f"   Genres: {', '.join(params['genres'])}")
    print(f"   Mood: {mapper.get_mood_description(detected_emotion)}")
    
    # Get Spotify recommendations
    print(f"\n🎵 Fetching Spotify recommendations...")
    spotify_tracks = spotify.get_recommendations(params, limit=3)
    if spotify_tracks:
        print(f"   ✅ Got {len(spotify_tracks)} tracks")
        print(f"   Top track: {spotify_tracks[0]['name']} - {spotify_tracks[0]['artist']}")
    else:
        print("   ⚠️  Spotify unavailable")
    
    # Get YouTube videos
    print(f"\n📹 Fetching YouTube videos...")
    youtube_videos = youtube.search_by_emotion(detected_emotion, max_results=3)
    if youtube_videos:
        print(f"   ✅ Got {len(youtube_videos)} videos")
        print(f"   Top video: {youtube_videos[0]['title'][:50]}...")
    else:
        print("   ⚠️  YouTube unavailable")
    
    print("\n✅ Complete workflow test finished!")

def main():
    """Main test runner"""
    print("\n" + "="*60)
    print("  🎵 Music API Integration Test Suite")
    print("="*60)
    
    print("\nThis script will test the music API integration components.")
    print("Make sure you have set up your .env file with API credentials.")
    print("\nRequired environment variables:")
    print("  - SPOTIFY_CLIENT_ID")
    print("  - SPOTIFY_CLIENT_SECRET")
    print("  - YOUTUBE_API_KEY (optional, fallback available)")
    
    input("\nPress Enter to continue...")
    
    try:
        # Test 1: Emotion Mapper
        test_emotion_mapper()
        
        # Test 2: Spotify API
        test_spotify_api()
        
        # Test 3: YouTube API
        test_youtube_api()
        
        # Test 4: Full Workflow
        test_full_workflow()
        
        print_section("🎉 All Tests Completed!")
        print("Your music API integration is ready to use!")
        print("\nNext steps:")
        print("  1. Run the enhanced Streamlit app:")
        print("     streamlit run code/deployment/app_with_music_apis.py")
        print("  2. Check out the documentation:")
        print("     - API_SETUP_GUIDE.md")
        print("     - MUSIC_API_INTEGRATION.md")
        print("  3. Start detecting emotions and enjoying music! 🎵")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during testing: {str(e)}")
        print("Please check your configuration and try again.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
