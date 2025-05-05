import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, \
    CouldNotRetrieveTranscript


def extract_video_id(url):
    pattern = r"(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([\w-]{11})"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def get_transcript(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)

        # Intenta encontrar el transcript en español o inglés
        for lang in ['es', 'en']:
            try:
                transcript = transcripts.find_transcript([lang]).fetch()
                return " ".join([entry['text'] for entry in transcript])
            except:
                continue

        # Si no se encuentra ninguno de esos, usa el primero disponible
        try:
            transcript = transcripts._manually_created_transcripts[0].fetch()
            return " ".join([entry['text'] for entry in transcript])
        except:
            pass

        try:
            transcript = transcripts._generated_transcripts[0].fetch()
            return " ".join([entry['text'] for entry in transcript])
        except:
            pass

        return "Transcript not available"

    except Exception as e:
        return f"Transcript error: {str(e)}"


def get_video_info(url):
    video_id = extract_video_id(url)
    if not video_id:
        return {"error": "Invalid YouTube URL"}

    # Datos básicos
    api_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    response = requests.get(api_url)
    if response.status_code != 200:
        return {"error": "Could not fetch video metadata"}

    video_data = response.json()
    transcript_text = get_transcript(video_id)

    return {
        "video_id": video_id,
        "title": video_data.get("title", "Unknown"),
        "author": video_data.get("author_name", "Unknown"),
        "video_description": video_data.get("title", "No description"),
        "video_transcript": transcript_text
    }
