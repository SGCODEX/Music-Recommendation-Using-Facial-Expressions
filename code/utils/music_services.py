"""
Music Service Integration Module
Support for multiple music streaming services
"""

import webbrowser
import urllib.parse
from typing import Optional, Dict, List
from enum import Enum


class MusicService(Enum):
    """Supported music streaming services"""
    YOUTUBE = "youtube"
    SPOTIFY = "spotify"
    APPLE_MUSIC = "apple_music"
    SOUNDCLOUD = "soundcloud"
    YOUTUBE_MUSIC = "youtube_music"


class MusicRecommendation:
    """Handle music recommendations across different platforms"""
    
    # Search query templates for different emotions
    EMOTION_QUERIES = {
        "Happy": ["upbeat songs", "happy music", "feel good hits", "cheerful tunes"],
        "Sad": ["sad songs", "emotional ballads", "melancholic music", "heartbreak songs"],
        "Angry": ["aggressive music", "heavy metal", "intense workout", "angry rap"],
        "Neutral": ["chill music", "relaxing sounds", "ambient music", "lo-fi beats"],
        "Surprise": ["epic music", "surprising hits", "unexpected gems", "unique sounds"],
        "Fear": ["calming music", "peaceful sounds", "meditation music", "soothing melodies"],
        "Disgust": ["cleansing music", "fresh sounds", "uplifting tracks", "positive vibes"]
    }
    
    @staticmethod
    def get_youtube_url(emotion: str, query_variant: int = 0) -> str:
        """
        Get YouTube search URL for emotion
        
        Args:
            emotion: Detected emotion
            query_variant: Index of query variant to use
            
        Returns:
            str: YouTube search URL
        """
        queries = MusicRecommendation.EMOTION_QUERIES.get(
            emotion, 
            ["background music"]
        )
        
        query = queries[query_variant % len(queries)]
        encoded_query = urllib.parse.quote(query)
        
        return f"https://www.youtube.com/results?search_query={encoded_query}"
    
    @staticmethod
    def get_youtube_music_url(emotion: str) -> str:
        """
        Get YouTube Music search URL
        
        Args:
            emotion: Detected emotion
            
        Returns:
            str: YouTube Music search URL
        """
        queries = MusicRecommendation.EMOTION_QUERIES.get(emotion, ["music"])
        query = queries[0]
        encoded_query = urllib.parse.quote(query)
        
        return f"https://music.youtube.com/search?q={encoded_query}"
    
    @staticmethod
    def get_spotify_url(emotion: str) -> str:
        """
        Get Spotify search URL
        
        Args:
            emotion: Detected emotion
            
        Returns:
            str: Spotify search URL
        """
        queries = MusicRecommendation.EMOTION_QUERIES.get(emotion, ["music"])
        query = queries[0]
        encoded_query = urllib.parse.quote(query)
        
        return f"https://open.spotify.com/search/{encoded_query}"
    
    @staticmethod
    def get_apple_music_url(emotion: str) -> str:
        """
        Get Apple Music search URL
        
        Args:
            emotion: Detected emotion
            
        Returns:
            str: Apple Music search URL
        """
        queries = MusicRecommendation.EMOTION_QUERIES.get(emotion, ["music"])
        query = queries[0]
        encoded_query = urllib.parse.quote(query)
        
        return f"https://music.apple.com/us/search?term={encoded_query}"
    
    @staticmethod
    def get_soundcloud_url(emotion: str) -> str:
        """
        Get SoundCloud search URL
        
        Args:
            emotion: Detected emotion
            
        Returns:
            str: SoundCloud search URL
        """
        queries = MusicRecommendation.EMOTION_QUERIES.get(emotion, ["music"])
        query = queries[0]
        encoded_query = urllib.parse.quote(query)
        
        return f"https://soundcloud.com/search?q={encoded_query}"
    
    @staticmethod
    def get_music_url(emotion: str, service: MusicService = MusicService.YOUTUBE) -> str:
        """
        Get music URL for any supported service
        
        Args:
            emotion: Detected emotion
            service: Music streaming service
            
        Returns:
            str: Music search URL
        """
        url_methods = {
            MusicService.YOUTUBE: MusicRecommendation.get_youtube_url,
            MusicService.SPOTIFY: MusicRecommendation.get_spotify_url,
            MusicService.APPLE_MUSIC: MusicRecommendation.get_apple_music_url,
            MusicService.SOUNDCLOUD: MusicRecommendation.get_soundcloud_url,
            MusicService.YOUTUBE_MUSIC: MusicRecommendation.get_youtube_music_url
        }
        
        method = url_methods.get(service, MusicRecommendation.get_youtube_url)
        return method(emotion)
    
    @staticmethod
    def open_music(emotion: str, service: MusicService = MusicService.YOUTUBE) -> bool:
        """
        Open music in browser
        
        Args:
            emotion: Detected emotion
            service: Music streaming service
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            url = MusicRecommendation.get_music_url(emotion, service)
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error opening music: {str(e)}")
            return False
    
    @staticmethod
    def get_all_service_urls(emotion: str) -> Dict[str, str]:
        """
        Get URLs for all supported services
        
        Args:
            emotion: Detected emotion
            
        Returns:
            dict: Service name to URL mapping
        """
        return {
            "YouTube": MusicRecommendation.get_youtube_url(emotion),
            "YouTube Music": MusicRecommendation.get_youtube_music_url(emotion),
            "Spotify": MusicRecommendation.get_spotify_url(emotion),
            "Apple Music": MusicRecommendation.get_apple_music_url(emotion),
            "SoundCloud": MusicRecommendation.get_soundcloud_url(emotion)
        }
    
    @staticmethod
    def get_query_variants(emotion: str) -> List[str]:
        """
        Get all query variants for an emotion
        
        Args:
            emotion: Detected emotion
            
        Returns:
            list: List of query strings
        """
        return MusicRecommendation.EMOTION_QUERIES.get(
            emotion,
            ["background music"]
        )


class PlaylistGenerator:
    """Generate playlists based on emotion patterns"""
    
    @staticmethod
    def create_mood_playlist(emotions: List[str], service: MusicService = MusicService.YOUTUBE) -> List[str]:
        """
        Create a playlist based on multiple emotions
        
        Args:
            emotions: List of detected emotions
            service: Music streaming service
            
        Returns:
            list: List of URLs for playlist
        """
        playlist = []
        
        # Get unique emotions while preserving order
        seen = set()
        unique_emotions = []
        for emotion in emotions:
            if emotion not in seen:
                seen.add(emotion)
                unique_emotions.append(emotion)
        
        # Generate URLs for each unique emotion
        for emotion in unique_emotions:
            url = MusicRecommendation.get_music_url(emotion, service)
            playlist.append(url)
        
        return playlist
    
    @staticmethod
    def get_mood_journey_playlist(start_emotion: str, end_emotion: str) -> List[str]:
        """
        Create a playlist that transitions from one emotion to another
        
        Args:
            start_emotion: Starting emotion
            end_emotion: Target emotion
            
        Returns:
            list: List of URLs for transitional playlist
        """
        # Define emotion transitions
        transition_map = {
            ("Sad", "Happy"): ["Neutral", "Surprise"],
            ("Angry", "Neutral"): ["Fear", "Sad"],
            ("Fear", "Happy"): ["Neutral", "Surprise"],
            ("Angry", "Happy"): ["Neutral"],
        }
        
        # Get transition emotions
        transition = transition_map.get((start_emotion, end_emotion), [])
        
        # Build playlist
        playlist_emotions = [start_emotion] + transition + [end_emotion]
        
        return [MusicRecommendation.get_youtube_url(emotion) 
                for emotion in playlist_emotions]


# Example usage
if __name__ == "__main__":
    emotion = "Happy"
    
    print(f"Music recommendations for '{emotion}':\n")
    
    # Get URLs for all services
    urls = MusicRecommendation.get_all_service_urls(emotion)
    for service, url in urls.items():
        print(f"{service}: {url}")
    
    print(f"\nQuery variants:")
    variants = MusicRecommendation.get_query_variants(emotion)
    for i, variant in enumerate(variants, 1):
        print(f"{i}. {variant}")
    
    print(f"\nOpening music in YouTube...")
    MusicRecommendation.open_music(emotion, MusicService.YOUTUBE)
    
    # Generate playlist
    emotions = ["Sad", "Neutral", "Happy"]
    print(f"\nPlaylist for emotions {emotions}:")
    playlist = PlaylistGenerator.create_mood_playlist(emotions)
    for i, url in enumerate(playlist, 1):
        print(f"{i}. {url}")
