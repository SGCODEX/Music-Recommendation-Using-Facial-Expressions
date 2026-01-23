"""
Music API Integration Module
Handles Spotify and YouTube Music API integrations for emotion-based music recommendations
"""

from .emotion_mapper import EmotionMapper
from .spotify_api import SpotifyMusicAPI
from .youtube_api import YouTubeMusicAPI

__all__ = ['EmotionMapper', 'SpotifyMusicAPI', 'YouTubeMusicAPI']
