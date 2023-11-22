
import vis
import data_mgr as dmgr
from const import CONST
import playlist_mgr as pmgr
import os
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import playlist_data as pldat
import csv



class Spotianalyze:
    ##################################################################################################################################

    # Welcome to Spotianalyze

    ##################################################################################################################################
    # Initialize User
    def __init__(self, username: str, client_id: str, client_secret: str, redirect_uri: str):
        '''
        Authentication for Spotify API
        '''

        self.USERNAME = username
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIERECT_URI = redirect_uri

        #add client id, client secret, and redirect uri into the environment variables to be accessed by spotipy
        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri


        # define scopes of data in which are allowed to be accessed
        scope = """
                user-read-private 
                user-read-playback-state 
                playlist-modify-public 
                user-library-modify 
                user-library-read 
                playlist-read-private 
                playlist-modify-private
                """
        # 
        try:
            token = util.prompt_for_user_token(username, scope)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)
        self._spotify_object = spotipy.Spotify(auth=token)
        
    
    
##################################################################################################################################
# Get csv of relevant data (song name, song artist(s), song id, features, times listened, times skipped) using dict
    def create_csv(self, filename: str):
        # Initialize fn vars
        page = 1
        song_list = []
        full_song_data = []

        # Create list of all songs in library
        while len(self.SPOTIFY_OBJECT.current_user_saved_tracks(limit=20, offset=(page-1))['items']) != 0:
            temp_song_list = ((self.SPOTIFY_OBJECT.current_user_saved_tracks(limit=20, offset=(page-1))['items']))
            song_list = song_list + temp_song_list
            page = page + 20

        # Create list of dicts for each song and associated data
        it = 1
        for track in song_list:
            # Display Progress
            print(f"{(it/len(song_list)) * 100}%", end=' ')

            # Iteration Reqs
            it = it + 1
            track_uri = track[self.TRACK][self.ID]
            track_features = self.SPOTIFY_OBJECT.audio_features(track_uri)

            # Dict Creation
            full_dict = {
                self.NAME: track[self.TRACK][self.NAME],
                self.ARTISTS: track[self.TRACK][self.ARTISTS],
                self.ID: track_uri,
                self.DURATION_MS: track[self.TRACK][self.DURATION_MS],
                self.DANCEABILITY: track_features[0][self.DANCEABILITY],
                self.ENERGY: track_features[0][self.ENERGY],
                self.KEY: track_features[0][self.KEY],
                self.LOUDNESS: track_features[0][self.LOUDNESS],
                self.SPEECHINESS: track_features[0][self.SPEECHINESS],
                self.INSTRUMENTALNESS: track_features[0][self.INSTRUMENTALNESS],
                self.ACOUSTICNESS: track_features[0][self.ACOUSTICNESS],
                self.LIVENESS: track_features[0][self.LIVENESS],
                self.VALENCE: track_features[0][self.VALENCE],
                self.TEMPO: track_features[0][self.TEMPO],
                self.TIME_SIGNATURE: track_features[0][self.TIME_SIGNATURE],
                self.TIMES_LISTENED: 0,
                self.TIMES_SKIPPED: 0
            }
            print(full_dict)
            full_song_data.append(full_dict)

        # Create csv file with data
        with open(filename, 'w') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=[self.NAME, self.ARTISTS, self.ID, self.DURATION_MS ] + self.KEYLIST + [self.TIMES_LISTENED, self.TIMES_SKIPPED])
            writer.writeheader()
            writer.writerows(full_song_data)
            



    # Fns to get current playing info in dict format
    # Fns to loop
    # Create way to extract data easily
    # Use that data to do stuff
    
##################################################################################################################################



