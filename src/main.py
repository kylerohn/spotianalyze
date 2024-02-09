import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotianalyze import create_library

# export SPOTIPY_CLIENT_ID='770e8d064cc34410a3954b64add60085'
# export SPOTIPY_CLIENT_SECRET='8a335a6376074a7b8f4696c51b05e860'
# export SPOTIPY_REDIRECT_URI='https://localhost/'

scope = """
                user-read-private 
                user-read-playback-state 
                playlist-modify-public 
                user-library-modify 
                user-library-read 
                playlist-read-private 
                playlist-modify-private
                """

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))




create_library(sp)
