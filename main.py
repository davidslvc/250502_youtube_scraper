import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    pattern = r"(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_video_info(url):
    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}
    
    api_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        return {"error": "Could not fetch video metadata"}
    
    video_data = response.json()
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])
    except:
        transcript_text = "Transcript not available"
    
    return {
        "video_id": video_id,
        "title": video_data.get("title", "Unknown"),
        "author": video_data.get("author_name", "Unknown"),
        "video_description": video_data.get("title", "No description"),
        "video_transcript": transcript_text
    }
