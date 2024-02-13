from spotianalyze import *
import pandas as pd
from const import CONST as C
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt

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

# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


df = pd.read_csv(filepath_or_buffer="data/artists.csv")
display(df)


# for i0, i in enumerate(A):
#     for j0, j in enumerate(A):
#         if (i0 == j0):
#             continue
#         z = sst.linregress(i, j)
#         if  0.75 < np.abs(z[2]):
#             print(f"{C.KEYLIST[i0]} and {C.KEYLIST[j0]}: {z[2]}")
        
