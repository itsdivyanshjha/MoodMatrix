import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Define more emotions and corresponding seed genres
EMOTION_TO_GENRES = {
    "happy": ["pop", "happy", "dance"],
    "sad": ["sad", "acoustic", "piano"],
    "angry": ["metal", "rock", "punk"],
    "relaxed": ["chill", "ambient", "acoustic"],
    "energetic": ["workout", "dance", "edm"],
    "romantic": ["romance", "rnb", "jazz"],
    "nostalgic": ["classic", "oldies", "retro"],
    # Add more emotions and corresponding genres as needed
}

def get_mood_from_prompt(prompt):
    # Simple keyword-based emotion detection for demonstration
    prompt = prompt.lower()
    for emotion in EMOTION_TO_GENRES:
        if emotion in prompt:
            return emotion
    return "happy"  # Default emotion if none matched

def generate_playlist(sp, mood):
    genres = EMOTION_TO_GENRES.get(mood, ["pop"])
    seed_genres = random.sample(genres, 1)
    recommendations = sp.recommendations(seed_genres=seed_genres, limit=20)
    track_ids = [track['id'] for track in recommendations['tracks']]
    return track_ids

def create_playlist(sp, user_id, name, description, track_ids, mood):
    playlist_name = f"{name} - {mood.capitalize()}"
    playlist_description = f"{description} Mood: {mood.capitalize()}"
    playlist = sp.user_playlist_create(user_id, playlist_name, description=playlist_description)
    sp.user_playlist_add_tracks(user_id, playlist['id'], track_ids)
    return playlist['external_urls']['spotify']
