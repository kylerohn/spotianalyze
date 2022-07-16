import csv
import os
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

import numpy as np
import matplotlib.pyplot as plt
import helperfns as hlp

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

    
##################################################################################################################################
# Get csv of relevant data (song name, song artist(s), song id, features, times listened, times skipped) using dict
    def create_csv(self, filename: str):
        # Create list of all songs in library
        song_list = hlp.get_library_song_list(self)
        # Create list of dicts for each song and associated data
        full_song_data = hlp.create_song_list_dict(self, song_list)
        # Create csv file with given data
        hlp.write_csv(full_song_data, filename)
            



spotianalyze = Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445', 'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')
# spotianalyze.create_csv('kyles_lib.csv')
# hlp.read_csv("kyles_lib.csv")
# tf = hlp.compare_csv_to_library(spotianalyze, "kyles_lib.csv")
# print(hlp.get_currently_playing_data(spotianalyze))
# _id = hlp.user_playlist_search(spotianalyze)
# _dict = hlp.get_playlist_info_dict(spotianalyze, _id)
# hlp.create_playlist_csv(spotianalyze, _id, _dict)
_nparr = hlp.numpify("Vibe.csv")
hlp.matplotlib_scatter_by_key(_nparr)


    # Fns to get current playing info in dict format
    # Fns to loop
    # Create way to extract data easily
    # Use that data to do stuff
    