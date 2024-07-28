from flask import Flask, request, redirect, url_for, session, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from utils import get_mood_from_prompt, generate_playlist, create_playlist

app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'

# Spotify API credentials
SPOTIPY_CLIENT_ID = "636fd1a5255a4637befcc7a0d34ff5d2"
SPOTIPY_CLIENT_SECRET = "a334cb8e641a4958997c2e12761eb5a2"
SPOTIPY_REDIRECT_URI = "http://localhost:8085/callback"  # Update this to your Redirect URI

# Scope for modifying public playlists
scope = "playlist-modify-public user-top-read user-library-read"

# Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=scope))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate')
def generate():
    try:
        prompt = request.args.get('prompt')
        print(f"Received prompt: {prompt}")
        mood = get_mood_from_prompt(prompt)
        print(f"Determined mood: {mood}")
        user = sp.current_user()
        track_ids = generate_playlist(sp, mood, user['id'])
        print(f"Generated track IDs: {track_ids}")
        if not track_ids:
            return f"<h1>No tracks found for mood: {mood}</h1>"

        playlist_url = create_playlist(sp, user['id'], "Mood-Based Playlist", "Generated based on your mood", track_ids, mood)
        if not playlist_url:
            return f"<h1>Failed to create playlist</h1>"

        print(f"Created playlist URL: {playlist_url}")
        return render_template('result.html', playlist_url=playlist_url)
    except Exception as e:
        print(f"An error occurred: {e}")
        return f"<h1>Internal Server Error</h1><p>{e}</p>"

if __name__ == '__main__':
    app.run(debug=True)
