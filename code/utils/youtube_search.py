import requests
import re

def fetch_youtube_url(emotion):
    search_query = f"https://www.youtube.com/results?search_query={emotion}+background+tunes"
    response = requests.get(search_query)
    if response.status_code != 200:
        return None
    match = re.search(r'/watch\?v=([^"]+)', response.text)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id.encode('utf-8').decode('unicode_escape')}"
    return None