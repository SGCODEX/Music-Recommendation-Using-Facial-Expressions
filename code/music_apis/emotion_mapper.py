"""
Emotion to Music Genre/Mood Mapper
Maps detected facial emotions to appropriate music genres, moods, and search queries
"""

class EmotionMapper:
    """Maps detected emotions to music attributes for API queries"""
    
    def __init__(self):
        self.emotion_to_spotify_params = {
            'Happy': {
                'genres': ['pop', 'dance', 'party', 'summer'],
                'seed_artists': ['5K4W6rqBFWDnAN6FQUkS6x'],  # Kanye West
                'target_valence': 0.8,
                'target_energy': 0.7,
                'target_danceability': 0.7,
                'mood': 'happy upbeat energetic',
                'min_popularity': 50
            },
            'Sad': {
                'genres': ['acoustic', 'indie', 'sad', 'piano'],
                'seed_artists': ['3TVXtAsR1Inumwj472S9r4'],  # Drake
                'target_valence': 0.2,
                'target_energy': 0.3,
                'target_acousticness': 0.7,
                'mood': 'sad melancholic emotional',
                'min_popularity': 40
            },
            'Angry': {
                'genres': ['metal', 'rock', 'hard-rock', 'punk'],
                'seed_artists': ['1Yox196W7bzVNZI7RBaPnf'],  # Metallica
                'target_valence': 0.3,
                'target_energy': 0.9,
                'target_loudness': -5,
                'mood': 'intense aggressive powerful',
                'min_popularity': 40
            },
            'Fear': {
                'genres': ['ambient', 'chill', 'lo-fi', 'instrumental'],
                'seed_artists': ['0YC192cP3KPCRWx8zr8MfZ'],  # Hans Zimmer
                'target_valence': 0.3,
                'target_energy': 0.4,
                'target_instrumentalness': 0.7,
                'mood': 'calm soothing peaceful',
                'min_popularity': 30
            },
            'Surprise': {
                'genres': ['electronic', 'edm', 'electro', 'techno'],
                'seed_artists': ['4dpARuHxo51G3z768sgnrY'],  # Avicii
                'target_valence': 0.6,
                'target_energy': 0.75,
                'target_danceability': 0.8,
                'mood': 'exciting unexpected energetic',
                'min_popularity': 50
            },
            'Disgust': {
                'genres': ['alternative', 'indie-rock', 'grunge'],
                'seed_artists': ['6olE6TJLqED3rqDCT0FyPh'],  # Nirvana
                'target_valence': 0.35,
                'target_energy': 0.6,
                'mood': 'edgy alternative dark',
                'min_popularity': 40
            },
            'Neutral': {
                'genres': ['indie', 'pop', 'singer-songwriter', 'folk'],
                'seed_artists': ['06HL4z0CvFAxyc27GXpf02'],  # Taylor Swift
                'target_valence': 0.5,
                'target_energy': 0.5,
                'mood': 'relaxed balanced chill',
                'min_popularity': 45
            }
        }
        
        self.emotion_to_youtube_queries = {
            'Happy': [
                'happy upbeat music',
                'feel good songs',
                'party playlist',
                'uplifting music'
            ],
            'Sad': [
                'sad songs',
                'emotional music',
                'heartbreak playlist',
                'melancholic songs'
            ],
            'Angry': [
                'metal music',
                'hard rock songs',
                'intense music',
                'aggressive playlist'
            ],
            'Fear': [
                'calming music',
                'relaxing ambient music',
                'peaceful instrumental',
                'soothing sounds'
            ],
            'Surprise': [
                'electronic dance music',
                'EDM hits',
                'surprising music',
                'upbeat electronic'
            ],
            'Disgust': [
                'alternative rock',
                'grunge playlist',
                'indie rock songs',
                'edgy music'
            ],
            'Neutral': [
                'chill music',
                'indie playlist',
                'relaxing songs',
                'background music'
            ]
        }
    
    def get_spotify_params(self, emotion):
        """
        Get Spotify API parameters for a given emotion
        
        Args:
            emotion (str): Detected emotion (Happy, Sad, Angry, etc.)
            
        Returns:
            dict: Parameters for Spotify API recommendations
        """
        return self.emotion_to_spotify_params.get(
            emotion, 
            self.emotion_to_spotify_params['Neutral']
        )
    
    def get_youtube_query(self, emotion):
        """
        Get YouTube search query for a given emotion
        
        Args:
            emotion (str): Detected emotion
            
        Returns:
            str: Primary search query for YouTube
        """
        queries = self.emotion_to_youtube_queries.get(
            emotion,
            self.emotion_to_youtube_queries['Neutral']
        )
        return queries[0]
    
    def get_all_youtube_queries(self, emotion):
        """
        Get all YouTube search queries for a given emotion
        
        Args:
            emotion (str): Detected emotion
            
        Returns:
            list: All search queries for the emotion
        """
        return self.emotion_to_youtube_queries.get(
            emotion,
            self.emotion_to_youtube_queries['Neutral']
        )
    
    def get_mood_description(self, emotion):
        """
        Get a human-readable mood description
        
        Args:
            emotion (str): Detected emotion
            
        Returns:
            str: Mood description
        """
        params = self.get_spotify_params(emotion)
        return params.get('mood', 'relaxed')
