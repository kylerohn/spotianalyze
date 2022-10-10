import vis
import data_mgr as dmgr
from const import CONST
import playlist_mgr as pmgr
import os
import spotipy
import spotipy.util as util
from sklearn.cluster import KMeans
from json.decoder import JSONDecodeError
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import playlist_data as pldat



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

        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

        scope = 'user-read-private user-read-playback-state playlist-modify-public user-library-modify user-library-read playlist-read-private playlist-modify-private'
        try:
            token = util.prompt_for_user_token(username, scope)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)
        spotify_object = spotipy.Spotify(auth=token)
        user = spotify_object.current_user()
        self.SPOTIFY_OBJECT = spotify_object

    def __repr__(self):
        return self.SPOTIFY_OBJECT

##################################################################################################################################



