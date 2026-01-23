"""
Spotify Web API Integration
Handles authentication and music recommendations from Spotify
"""

import requests
import base64
import time
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)


class SpotifyMusicAPI:
    """Spotify API client for emotion-based music recommendations"""
    
    def __init__(self, client_id=None, client_secret=None):
        """
        Initialize Spotify API client
        
        Args:
            client_id (str): Spotify API Client ID
            client_secret (str): Spotify API Client Secret
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.token_expiry = 0
        
        self.base_url = 'https://api.spotify.com/v1'
        self.auth_url = 'https://accounts.spotify.com/api/token'
    
    def authenticate(self):
        """
        Authenticate with Spotify using Client Credentials flow
        
        Returns:
            bool: True if authentication successful, False otherwise
        """
        if not self.client_id or not self.client_secret:
            logger.warning("Spotify credentials not provided")
            return False
        
        # Check if token is still valid
        if self.access_token and time.time() < self.token_expiry:
            return True
        
        try:
            # Encode credentials
            auth_str = f"{self.client_id}:{self.client_secret}"
            auth_bytes = auth_str.encode('utf-8')
            auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')
            
            # Request token
            headers = {
                'Authorization': f'Basic {auth_base64}',
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            data = {'grant_type': 'client_credentials'}
            
            response = requests.post(self.auth_url, headers=headers, data=data, timeout=10)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data['access_token']
            # Set expiry time (subtract 60 seconds for buffer)
            self.token_expiry = time.time() + token_data.get('expires_in', 3600) - 60
            
            logger.info("Successfully authenticated with Spotify")
            return True
            
        except Exception as e:
            logger.error(f"Spotify authentication failed: {str(e)}")
            return False
    
    def get_recommendations(self, emotion_params, limit=10):
        """
        Get music recommendations based on emotion parameters
        
        Args:
            emotion_params (dict): Emotion mapping parameters from EmotionMapper
            limit (int): Number of recommendations to fetch
            
        Returns:
            list: List of track dictionaries with track info
        """
        if not self.authenticate():
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            # Build query parameters
            params = {
                'limit': limit,
                'seed_genres': ','.join(emotion_params.get('genres', ['pop'])[:5])
            }
            
            # Add optional parameters
            if 'target_valence' in emotion_params:
                params['target_valence'] = emotion_params['target_valence']
            if 'target_energy' in emotion_params:
                params['target_energy'] = emotion_params['target_energy']
            if 'target_danceability' in emotion_params:
                params['target_danceability'] = emotion_params['target_danceability']
            if 'target_acousticness' in emotion_params:
                params['target_acousticness'] = emotion_params['target_acousticness']
            if 'target_instrumentalness' in emotion_params:
                params['target_instrumentalness'] = emotion_params['target_instrumentalness']
            if 'min_popularity' in emotion_params:
                params['min_popularity'] = emotion_params['min_popularity']
            
            url = f"{self.base_url}/recommendations"
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            tracks = []
            
            for track in data.get('tracks', []):
                track_info = {
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'preview_url': track.get('preview_url'),
                    'spotify_url': track['external_urls']['spotify'],
                    'duration_ms': track['duration_ms'],
                    'uri': track['uri']
                }
                tracks.append(track_info)
            
            logger.info(f"Retrieved {len(tracks)} Spotify recommendations")
            return tracks
            
        except Exception as e:
            logger.error(f"Failed to get Spotify recommendations: {str(e)}")
            return []
    
    def search_tracks(self, query, limit=10):
        """
        Search for tracks on Spotify
        
        Args:
            query (str): Search query
            limit (int): Number of results
            
        Returns:
            list: List of track dictionaries
        """
        if not self.authenticate():
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            params = {
                'q': query,
                'type': 'track',
                'limit': limit
            }
            
            url = f"{self.base_url}/search"
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            tracks = []
            
            for track in data.get('tracks', {}).get('items', []):
                track_info = {
                    'name': track['name'],
                    'artist': ', '.join([artist['name'] for artist in track['artists']]),
                    'album': track['album']['name'],
                    'album_art': track['album']['images'][0]['url'] if track['album']['images'] else None,
                    'preview_url': track.get('preview_url'),
                    'spotify_url': track['external_urls']['spotify'],
                    'duration_ms': track['duration_ms'],
                    'uri': track['uri']
                }
                tracks.append(track_info)
            
            return tracks
            
        except Exception as e:
            logger.error(f"Failed to search Spotify tracks: {str(e)}")
            return []
    
    def get_playlist_by_mood(self, mood, limit=1):
        """
        Search for playlists matching a specific mood
        
        Args:
            mood (str): Mood/emotion to search for
            limit (int): Number of playlists to return
            
        Returns:
            list: List of playlist dictionaries
        """
        if not self.authenticate():
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            params = {
                'q': f'{mood} music',
                'type': 'playlist',
                'limit': limit
            }
            
            url = f"{self.base_url}/search"
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            playlists = []
            
            for playlist in data.get('playlists', {}).get('items', []):
                playlist_info = {
                    'name': playlist['name'],
                    'description': playlist.get('description', ''),
                    'owner': playlist['owner']['display_name'],
                    'tracks_total': playlist['tracks']['total'],
                    'playlist_url': playlist['external_urls']['spotify'],
                    'image': playlist['images'][0]['url'] if playlist['images'] else None,
                    'uri': playlist['uri']
                }
                playlists.append(playlist_info)
            
            return playlists
            
        except Exception as e:
            logger.error(f"Failed to get Spotify playlists: {str(e)}")
            return []
