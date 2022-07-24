import os
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import second_layer as sl
import time

class Spotianalyze:
##################################################################################################################################

# Welcome to Spotianalyze

##################################################################################################################################
# Initialize User 
    def __init__(self, username: str, client_id: str, client_secret: str, redirect_uri: str):

        self.USERNAME = username
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIERECT_URI = redirect_uri

        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

        scope = 'user-read-private user-read-playback-state playlist-modify-public user-library-modify user-library-read playlist-read-private'
        try:
            token = util.prompt_for_user_token(username, scope)
        except(AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)
        spotify_object = spotipy.Spotify(auth=token)
        user = spotify_object.current_user()
        self.SPOTIFY_OBJECT = spotify_object

    def __repr__(self):
        return self.SPOTIFY_OBJECT

    


spotianalyze = Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445', 'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')

playlist_id = sl.user_playlist_search(spotianalyze)
sl.create_playlist_songs_dataframe(spotianalyze, playlist_id)





# sl.create_liked_songs_dataframe(spotianalyze)

# dataframe = pd.read_csv("data/liked_songs.csv")

# matrix = sl.numpyify(dataframe)

# sl.plt_histogram_by_key(matrix)

# while True:
#     current_data = sl.get_currently_playing_data(spotianalyze)
#     print(current_data["name"])
#     print(current_data["progress_ms"])
#     time.sleep(0.1)

    # Fns to get current playing info in dict format
    # Fns to loop
    # Create way to extract data easily
    # Use that data to do stuff
    