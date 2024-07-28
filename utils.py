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
    "hopeful": ["indie", "folk", "acoustic"],
    "lonely": ["blues", "singer-songwriter", "acoustic"],
    "excited": ["electronic", "house", "pop"],
    "calm": ["ambient", "new age", "acoustic"],
    "motivated": ["hip-hop", "rap", "workout"],
    "peaceful": ["classical", "ambient", "new age"],
    "confident": ["rock", "alternative", "hip-hop"],
    "melancholy": ["indie", "folk", "blues"],
    "joyful": ["pop", "dance", "electronic"],
    "reflective": ["jazz", "blues", "classical"],
    "surprised": ["experimental", "electronic", "pop"],
    "adventurous": ["world", "reggae", "latin"],
    "optimistic": ["indie", "pop", "folk"]
}

def get_mood_from_prompt(prompt):
    # Simple keyword-based emotion detection for demonstration
    prompt = prompt.lower()
    for emotion in EMOTION_TO_GENRES:
        if emotion in prompt:
            return emotion
    return "happy"  # Default emotion if none matched

def generate_playlist(sp, mood, user_id):
    genres = EMOTION_TO_GENRES.get(mood, ["pop"])
    seed_genres = random.sample(genres, 1)
    
    # Fetch user's top artists and tracks
    top_artists = sp.current_user_top_artists(limit=10, time_range='medium_term')['items']
    top_tracks = sp.current_user_top_tracks(limit=10, time_range='medium_term')['items']
    
    top_artists_ids = [artist['id'] for artist in top_artists]
    top_tracks_ids = [track['id'] for track in top_tracks]

    # Get recommendations based on mood and user's top tracks/artists
    recommendations = sp.recommendations(seed_artists=top_artists_ids[:2], seed_genres=seed_genres, seed_tracks=top_tracks_ids[:2], limit=20)['tracks']
    recommended_track_ids = [track['id'] for track in recommendations]
    
    # Include some new and trending tracks to introduce variety
    new_releases = sp.new_releases(limit=10)['albums']['items']
    trending_tracks = [track['id'] for album in new_releases for track in sp.album_tracks(album['id'])['items']]

    # Mix user favorites with new recommendations
    track_ids = top_tracks_ids + recommended_track_ids + random.sample(trending_tracks, 5)
    random.shuffle(track_ids)
    
    return track_ids

def create_playlist(sp, user_id, name, description, track_ids, mood):
    playlist_name = f"{name} - {mood.capitalize()}"
    playlist_description = f"{description} Mood: {mood.capitalize()}"
    playlist = sp.user_playlist_create(user_id, playlist_name, description=playlist_description)
    sp.user_playlist_add_tracks(user_id, playlist['id'], track_ids)
    return playlist['external_urls']['spotify']
