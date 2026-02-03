"""
Tests for music services integration
"""

import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from code.utils.music_services import (
    MusicService,
    MusicRecommendation,
    PlaylistGenerator
)


class TestMusicRecommendation(unittest.TestCase):
    """Test cases for MusicRecommendation"""
    
    def test_get_youtube_url(self):
        """Test YouTube URL generation"""
        url = MusicRecommendation.get_youtube_url("Happy")
        self.assertIn("youtube.com", url)
        self.assertIn("search_query", url)
    
    def test_get_spotify_url(self):
        """Test Spotify URL generation"""
        url = MusicRecommendation.get_spotify_url("Happy")
        self.assertIn("spotify.com", url)
        self.assertIn("search", url)
    
    def test_get_apple_music_url(self):
        """Test Apple Music URL generation"""
        url = MusicRecommendation.get_apple_music_url("Happy")
        self.assertIn("music.apple.com", url)
        self.assertIn("search", url)
    
    def test_get_soundcloud_url(self):
        """Test SoundCloud URL generation"""
        url = MusicRecommendation.get_soundcloud_url("Happy")
        self.assertIn("soundcloud.com", url)
        self.assertIn("search", url)
    
    def test_get_youtube_music_url(self):
        """Test YouTube Music URL generation"""
        url = MusicRecommendation.get_youtube_music_url("Happy")
        self.assertIn("music.youtube.com", url)
        self.assertIn("search", url)
    
    def test_get_music_url_all_services(self):
        """Test URL generation for all services"""
        for service in MusicService:
            url = MusicRecommendation.get_music_url("Happy", service)
            self.assertIsInstance(url, str)
            self.assertTrue(len(url) > 0)
    
    def test_get_all_service_urls(self):
        """Test getting URLs for all services"""
        urls = MusicRecommendation.get_all_service_urls("Happy")
        
        self.assertIn("YouTube", urls)
        self.assertIn("Spotify", urls)
        self.assertIn("Apple Music", urls)
        self.assertIn("SoundCloud", urls)
        self.assertEqual(len(urls), 5)
    
    def test_query_variants(self):
        """Test query variants for emotions"""
        variants = MusicRecommendation.get_query_variants("Happy")
        self.assertIsInstance(variants, list)
        self.assertTrue(len(variants) > 0)
        
        for variant in variants:
            self.assertIsInstance(variant, str)
    
    def test_all_emotions_have_queries(self):
        """Test that all emotions have query variants"""
        emotions = ["Happy", "Sad", "Angry", "Neutral", "Surprise", "Fear", "Disgust"]
        
        for emotion in emotions:
            variants = MusicRecommendation.get_query_variants(emotion)
            self.assertTrue(len(variants) > 0)
    
    def test_query_variant_rotation(self):
        """Test query variant rotation"""
        emotion = "Happy"
        variants = MusicRecommendation.get_query_variants(emotion)
        
        # Test that variant index wraps around
        for i in range(len(variants) * 2):
            url = MusicRecommendation.get_youtube_url(emotion, i)
            self.assertIn("youtube.com", url)


class TestPlaylistGenerator(unittest.TestCase):
    """Test cases for PlaylistGenerator"""
    
    def test_create_mood_playlist(self):
        """Test mood playlist creation"""
        emotions = ["Happy", "Sad", "Neutral"]
        playlist = PlaylistGenerator.create_mood_playlist(emotions)
        
        self.assertEqual(len(playlist), 3)
        for url in playlist:
            self.assertIn("youtube.com", url)
    
    def test_create_mood_playlist_duplicates(self):
        """Test playlist with duplicate emotions"""
        emotions = ["Happy", "Happy", "Sad", "Happy"]
        playlist = PlaylistGenerator.create_mood_playlist(emotions)
        
        # Should only have unique emotions
        self.assertEqual(len(playlist), 2)
    
    def test_create_mood_playlist_different_service(self):
        """Test playlist with different music service"""
        emotions = ["Happy", "Sad"]
        playlist = PlaylistGenerator.create_mood_playlist(
            emotions, 
            MusicService.SPOTIFY
        )
        
        self.assertEqual(len(playlist), 2)
        for url in playlist:
            self.assertIn("spotify.com", url)
    
    def test_mood_journey_playlist(self):
        """Test mood journey playlist"""
        playlist = PlaylistGenerator.get_mood_journey_playlist("Sad", "Happy")
        
        self.assertIsInstance(playlist, list)
        self.assertTrue(len(playlist) >= 2)  # At least start and end
        
        for url in playlist:
            self.assertIn("youtube.com", url)
    
    def test_empty_playlist(self):
        """Test with empty emotions list"""
        playlist = PlaylistGenerator.create_mood_playlist([])
        self.assertEqual(len(playlist), 0)


class TestMusicServiceEnum(unittest.TestCase):
    """Test cases for MusicService enum"""
    
    def test_music_service_values(self):
        """Test MusicService enum values"""
        self.assertEqual(MusicService.YOUTUBE.value, "youtube")
        self.assertEqual(MusicService.SPOTIFY.value, "spotify")
        self.assertEqual(MusicService.APPLE_MUSIC.value, "apple_music")
        self.assertEqual(MusicService.SOUNDCLOUD.value, "soundcloud")
        self.assertEqual(MusicService.YOUTUBE_MUSIC.value, "youtube_music")
    
    def test_all_services_supported(self):
        """Test that all services are in URL generation methods"""
        for service in MusicService:
            url = MusicRecommendation.get_music_url("Happy", service)
            self.assertIsInstance(url, str)
            self.assertTrue(len(url) > 0)


if __name__ == '__main__':
    unittest.main()
