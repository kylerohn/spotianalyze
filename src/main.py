from spotianalyze import *
import pandas as pd
from const import CONST as C
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import spotipy
from spotipy import SpotifyOAuth
import ast

# export SPOTIPY_CLIENT_ID='770e8d064cc34410a3954b64add60085'
# export SPOTIPY_CLIENT_SECRET='8a335a6376074a7b8f4696c51b05e860'
# export SPOTIPY_REDIRECT_URI='https://localhost/'
#  DANCEABILITY,# ENERGY,# KEY,# LOUDNESS,# SPEECHINESS,# ACOUSTICNESS,# INSTRUMENTALNESS,# LIVENESS,# VALENCE,# TEMPO
#DNB 0.521,0.892,3,-4.029,0.0433,0.0539,0.0,0.117,0.369,96.991 
# 0.762,0.74,4,-5.8,0.271,0.014,0.0,0.119,0.382,82.503
#Factors that impact musical difference are: Key, (Speechiness has high diff btwn songs)
#Liveness, Valence

LIBRARY_FILEPATH = "data/library.csv"
ARTIST_FILEPATH = "data/artists.csv"

scope = """
        user-read-private 
        user-read-playback-state 
        playlist-modify-public 
        user-library-modify 
        user-library-read 
        playlist-read-private 
        playlist-modify-private
        """

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

songs = dataframe_to_objects(LIBRARY_FILEPATH, ARTIST_FILEPATH)

for song in songs:
    print(f"Song: {song.name}, Artists: ", end=" ")
    for artist in song.artists:
        print(f"{artist.name};", end=" ")
        
    print()


exit()

        
