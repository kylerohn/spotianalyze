from spotianalyze import *
import pandas as pd
from const import CONST as C
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import spotipy
from spotipy import SpotifyOAuth
import ast
from AgglomerativeCluster import AgglomerativeCluster
from Cluster import Cluster



# export SPOTIPY_CLIENT_ID='770e8d064cc34410a3954b64add60085'
# export SPOTIPY_CLIENT_SECRET='8a335a6376074a7b8f4696c51b05e860'
# export SPOTIPY_REDIRECT_URI='https://localhost/'

# DANCEABILITY,
# ENERGY,
# KEY,
# ACOUSTICNESS,
# VALENCE,
# TEMPO

# Speechiness
# Instrumentalness

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
df = pd.read_csv(LIBRARY_FILEPATH)
for idx, tempo in enumerate(df[C.TEMPO]):
    df[C.TEMPO][idx] = tempo ** (1/3)

h = AgglomerativeCluster(df, C.ALTERED_KEYLIST, C.URI)
clusters = h.hierarchical_cluster(n=50, linkage="max", distance="manhattan")

ldf = pd.read_csv(LIBRARY_FILEPATH)
adf = pd.read_csv(ARTIST_FILEPATH)

for cluster in clusters:
    genre_dict = {}
    for c_uri in cluster.names:
        for lidx, ldf_uri in enumerate(ldf[C.URI]):
            if c_uri == ldf_uri:
                artists = ast.literal_eval(ldf[C.ARTISTS][lidx])
                for artist in artists:
                    for aidx, adf_uri in enumerate(adf[C.URI]):
                        if adf_uri == artist:
                            genres = ast.literal_eval(adf[C.GENRES][aidx])
                            for genre in genres:
                                if genre not in genre_dict.keys():
                                    genre_dict.update({genre : 1})
                                else:
                                    genre_dict[genre] += 1
                break
    print(genre_dict)