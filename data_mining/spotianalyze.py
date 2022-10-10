
import os
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError
import realtime as rt
import time
from const import CONST


class Spotianalyze:
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

# Init
spotianalyze = Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445',
                            'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')


# Create spotify object
spotify_object = spotianalyze.SPOTIFY_OBJECT

# Init data
raw_json = spotify_object.current_user_playing_track()
track_id = raw_json[CONST.ITEM][CONST.ID]
previous_data = {}

# Loop forever >:)
while True:
    try:
        track_id, previous_data = rt.get_currently_playing_data(spotianalyze, track_id, previous_data)
        time.sleep(1)
        # print("works")
    except:
        spotianalyze = Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445',
                            'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')
        time.sleep(1)
        # print("broke")