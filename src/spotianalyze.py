
from const import CONST as C
import os
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv



class Spotianalyze:
    ##################################################################################################################################

    # Welcome to Spotianalyze

    ##################################################################################################################################
    # Initialize User
    def __init__(self, _username: str, _client_id: str, _client_secret: str, _redirect_uri: str):
        '''
        Authentication for Spotify API
        '''

        self.USERNAME = _username
        self.CLIENT_ID = _client_id
        self.CLIENT_SECRET = _client_secret
        self.REDIERECT_URI = _redirect_uri

        #add client id, client secret, and redirect uri into the environment variables to be accessed by spotipy
        os.environ['SPOTIPY_CLIENT_ID'] = _client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = _client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = _redirect_uri


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
            token = util.prompt_for_user_token(_username, scope)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{_username}")
            token = util.prompt_for_user_token(_username, scope)
        self._spotify_object = spotipy.Spotify(auth=token)
            



    def liked_songs_parser(self):
        """
        Retrieve information about the user's liked songs from Spotify.

        Parameters:
            spotify_object (spotipy.Spotify): Authenticated Spotipy object.

        Returns:
            Dataframe: Dataframe containing information about the user's liked songs.

        Note:
            This function uses the Spotify Web API to retrieve information about the user's
            liked songs, ...

        """
        spotify_object = self._spotify_object

        # Initialize a dictionary to store information about the user's liked songs
        complete_dict = {
            C.ARTISTS: [],
            C.DURATION_MS: [],
            C.EXPLICIT: [],
            C.NAME: [],
            C.POPULARITY: [],
            C.URI: []
        }

        # Set the limit for the number of tracks to retrieve in each request
        limit = 50

        # Retrieve the initial set of tracks
        saved_tracks = spotify_object.current_user_saved_tracks(limit=limit)

        # Flag to control the loop
        next_page = True

        # Iterate through the pages of saved tracks
        while next_page:
            # Extract information about the tracks from the current set
            saved_tracks_info = saved_tracks[C.ITEMS]

            # Extract and store relevant data in the dictionary
            for track_info in saved_tracks_info:
                complete_dict = response_transformer(track_info[C.TRACK], complete_dict)
                print(complete_dict[C.NAME][-1])

            # Print the names of the tracks (for demonstration purposes)

            # Check if there are more pages
            if not saved_tracks['next']:
                next_page = False
            else:
                # Move to the next page of saved tracks
                saved_tracks = spotify_object.next(saved_tracks)
        
        # artist information processing
        complete_dict = self._artist_parser(complete_dict)

        # Return a dataframe containing information about the user's liked songs
        return pd.DataFrame.from_dict(complete_dict)




    def _artist_parser(self, complete_dict: dict):
        spotify_object = self._spotify_object
        
        # retrieve dictionary of artists
        for idx, artists in enumerate(complete_dict[C.ARTISTS]):
            artist_info_dict = {C.NAME: [],
                                C.GENRES: [],
                                C.POPULARITY:[],
                                C.URI: []}
            for artist in artists:
                artist_info_dict = response_transformer(artist, artist_info_dict)
            print(artist_info_dict[C.NAME])
            for artist_uri in artist_info_dict[C.URI]:
                artist_info = spotify_object.artist(artist_uri)
                artist_info_dict[C.GENRES] += [artist_info[C.GENRES]]
                artist_info_dict[C.POPULARITY] += [(artist_info[C.POPULARITY])]
                
            complete_dict[C.ARTISTS][idx] = pd.DataFrame.from_dict(artist_info_dict)
        


        return complete_dict



def response_transformer(response_dict: dict, empty_dict: dict):
    for key in empty_dict:
        try:
            empty_dict[key].append(response_dict[key])
        except:
            pass
    return empty_dict
