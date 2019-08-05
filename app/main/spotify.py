from app import app, cache

import requests

timeout = 60*app.config['YOUTUBE_DATA_FETCH_PER_DAY']/24

@cache.cached(timeout=timeout, key_prefix='getAllSpotifyPlaylists')
def getAllSpotifyPlaylists():
    listOfSpotifyPlaylists = []
    playlist_url = ''
    playlist_params = {
        'id': app.config['SPOTIFY_CLIENT_ID']
    }
    playlist_res = requests.get(playlist_url, params=playlist_params).json() or {}
    return listOfSpotifyPlaylists