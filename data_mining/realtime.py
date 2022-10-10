from const import CONST
import time
import pandas as pd

####################################################################################################################
# Get Data of the Currently Playing Song
def get_currently_playing_data(spotianalyze_object, current_song_id, previous_data = {}):
    # Get spotify object variable
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    # Variable Init
    raw_json = spotify_object.current_user_playing_track()
    track_id = raw_json[CONST.ITEM][CONST.ID]
    playlist_uri = None
    context = raw_json[CONST.CONTEXT][CONST.TYPE]
    if context == "playlist":
        playlist_uri = raw_json[CONST.CONTEXT][CONST.URI]
    progress = raw_json[CONST.PROGRESS_MS]

    current_playing_data = {
    CONST.ID: [track_id],
    CONST.PROGRESS_MS: [progress],
    CONST.CONTEXT: [context],
    CONST.PLAYLIST_URI: [playlist_uri],
    CONST.TIME: [float(time.time())]
    }
    
    # Check for song change
    if current_song_id != track_id:
        
        # Create Dataframe from song that just ended
        df = pd.DataFrame(previous_data)

        # Do I rlly gotta explain
        print(df)

        # Append song to song history csv file
        df.to_csv("song_history.csv", mode='a',header=False, index=False)

        # Next!
        current_song_id = track_id

    # Yk already lmao
    return current_song_id, current_playing_data
    
    

