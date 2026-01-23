"""
YouTube Data API Integration
Handles music video search and recommendations from YouTube
"""

import requests
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class YouTubeMusicAPI:
    """YouTube Data API client for emotion-based music recommendations"""
    
    def __init__(self, api_key=None):
        """
        Initialize YouTube API client
        
        Args:
            api_key (str): YouTube Data API key
        """
        self.api_key = api_key
        self.base_url = 'https://www.googleapis.com/youtube/v3'
    
    def search_videos(self, query, max_results=10):
        """
        Search for music videos on YouTube
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
            
        Returns:
            list: List of video dictionaries with video info
        """
        if not self.api_key:
            logger.warning("YouTube API key not provided, using fallback method")
            return self._fallback_search(query, max_results)
        
        try:
            params = {
                'part': 'snippet',
                'q': query,
                'type': 'video',
                'videoCategoryId': '10',  # Music category
                'maxResults': max_results,
                'key': self.api_key,
                'order': 'relevance'
            }
            
            url = f"{self.base_url}/search"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            videos = []
            
            for item in data.get('items', []):
                video_id = item['id']['videoId']
                snippet = item['snippet']
                
                video_info = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'channel': snippet['channelTitle'],
                    'thumbnail': snippet['thumbnails']['high']['url'],
                    'published_at': snippet['publishedAt'],
                    'video_url': f'https://www.youtube.com/watch?v={video_id}',
                    'embed_url': f'https://www.youtube.com/embed/{video_id}'
                }
                videos.append(video_info)
            
            logger.info(f"Retrieved {len(videos)} YouTube videos")
            return videos
            
        except Exception as e:
            logger.error(f"Failed to search YouTube videos: {str(e)}")
            return self._fallback_search(query, max_results)
    
    def _fallback_search(self, query, max_results=10):
        """
        Fallback search method using web scraping (when API key is not available)
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
            
        Returns:
            list: List of video dictionaries
        """
        try:
            import re
            
            search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            response = requests.get(search_url, timeout=10)
            response.raise_for_status()
            
            html_content = response.text
            
            # Extract video IDs using regex
            video_pattern = r'"videoId":"([^"]+)"'
            title_pattern = r'"title":{"runs":\[{"text":"([^"]+)"}]'
            
            video_ids = re.findall(video_pattern, html_content)
            titles = re.findall(title_pattern, html_content)
            
            videos = []
            for i, video_id in enumerate(video_ids[:max_results]):
                if video_id and len(video_id) == 11:  # Valid YouTube video ID length
                    video_info = {
                        'video_id': video_id,
                        'title': titles[i] if i < len(titles) else 'Music Video',
                        'description': '',
                        'channel': 'YouTube',
                        'thumbnail': f'https://img.youtube.com/vi/{video_id}/hqdefault.jpg',
                        'published_at': '',
                        'video_url': f'https://www.youtube.com/watch?v={video_id}',
                        'embed_url': f'https://www.youtube.com/embed/{video_id}'
                    }
                    videos.append(video_info)
            
            logger.info(f"Retrieved {len(videos)} YouTube videos using fallback method")
            return videos
            
        except Exception as e:
            logger.error(f"Fallback search also failed: {str(e)}")
            return []
    
    def get_video_details(self, video_id):
        """
        Get detailed information about a specific video
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            dict: Video details
        """
        if not self.api_key:
            return {
                'video_id': video_id,
                'video_url': f'https://www.youtube.com/watch?v={video_id}',
                'embed_url': f'https://www.youtube.com/embed/{video_id}'
            }
        
        try:
            params = {
                'part': 'snippet,contentDetails,statistics',
                'id': video_id,
                'key': self.api_key
            }
            
            url = f"{self.base_url}/videos"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('items'):
                return None
            
            item = data['items'][0]
            snippet = item['snippet']
            content_details = item.get('contentDetails', {})
            statistics = item.get('statistics', {})
            
            video_info = {
                'video_id': video_id,
                'title': snippet['title'],
                'description': snippet['description'],
                'channel': snippet['channelTitle'],
                'thumbnail': snippet['thumbnails']['high']['url'],
                'published_at': snippet['publishedAt'],
                'duration': content_details.get('duration', ''),
                'view_count': statistics.get('viewCount', 0),
                'like_count': statistics.get('likeCount', 0),
                'video_url': f'https://www.youtube.com/watch?v={video_id}',
                'embed_url': f'https://www.youtube.com/embed/{video_id}'
            }
            
            return video_info
            
        except Exception as e:
            logger.error(f"Failed to get video details: {str(e)}")
            return None
    
    def search_by_emotion(self, emotion, max_results=10):
        """
        Search for music videos based on emotion
        
        Args:
            emotion (str): Detected emotion
            max_results (int): Maximum number of results
            
        Returns:
            list: List of video dictionaries
        """
        # Construct emotion-specific search query
        query_map = {
            'Happy': 'happy upbeat music songs',
            'Sad': 'sad emotional music songs',
            'Angry': 'intense metal rock music',
            'Fear': 'calming relaxing ambient music',
            'Surprise': 'exciting electronic music edm',
            'Disgust': 'alternative indie rock music',
            'Neutral': 'chill indie music playlist'
        }
        
        query = query_map.get(emotion, f'{emotion} music')
        return self.search_videos(query, max_results)
