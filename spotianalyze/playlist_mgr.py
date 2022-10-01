from typing import List
import pandas as pd
from const import CONST

# Create Playlist
def create_playlist(spotianalyze_object, playlist_name):
    '''
    create playlist, use spotianalyze object and name as str
    '''
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    current_user = spotify_object.current_user()
    user_id = current_user[CONST.ID]

    try:
        info = spotify_object.user_playlist_create(user_id, playlist_name, public=True)
    except:
        return False
    
    return info[CONST.ID]

def add_to(spotianalyze_object, playlist_id, songs):

    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    playlist_id = str(playlist_id)

    for song in songs:
        a = spotify_object.playlist_add_items(playlist_id, [song], position=0)
        print(a)
     

