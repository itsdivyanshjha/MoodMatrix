# utils.py
from textblob import TextBlob

def get_mood_from_prompt(prompt):
    analysis = TextBlob(prompt)
    if analysis.sentiment.polarity > 0:
        mood = "happy"
    elif analysis.sentiment.polarity < 0:
        mood = "sad"
    else:
        mood = "neutral"
    return mood

def generate_playlist(sp, mood):
    try:
        if mood == "happy":
            query = "track:happy"
            mood_features = {'min_valence': 0.5, 'max_valence': 1.0}
        elif mood == "sad":
            query = "track:sad"
            mood_features = {'min_valence': 0.0, 'max_valence': 0.5}
        else:
            query = "track:calm"
            mood_features = {'min_valence': 0.4, 'max_valence': 0.6}

        results = sp.search(q=query, limit=50, type='track')
        print(f"Search results: {results}")
        track_ids = [track['id'] for track in results['tracks']['items']]
        print(f"Track IDs: {track_ids}")
        
        # Filter tracks by audio features
        audio_features = sp.audio_features(track_ids)
        print(f"Audio features: {audio_features}")
        
        # Ensure audio_features are not None
        if audio_features is None:
            print("Audio features are None")
            return []

        filtered_tracks = [track_id for track_id, features in zip(track_ids, audio_features) 
                           if features and mood_features['min_valence'] <= features['valence'] <= mood_features['max_valence']]
        
        print(f"Filtered tracks: {filtered_tracks}")
        return filtered_tracks
    except Exception as e:
        print(f"An error occurred in generate_playlist: {e}")
        return []

def create_playlist(sp, user_id, name, description, track_ids):
    try:
        if not track_ids:
            print("No tracks to add to the playlist")
            return None
        playlist = sp.user_playlist_create(user=user_id, name=name, description=description)
        sp.playlist_add_items(playlist_id=playlist['id'], items=track_ids)
        return playlist['external_urls']['spotify']
    except Exception as e:
        print(f"An error occurred in create_playlist: {e}")
        return None
