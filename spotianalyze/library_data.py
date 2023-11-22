import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from const import CONST
import features as sft
import data_mgr as dm


####################################################################################################################
# Data Acquisition
####################################################################################################################
def create_liked_songs_dataframe(spotianalyze_object):
    '''
    Create DataFrame objects of retreived data (Songs/Features and Artists) and save as CSV files
    '''

    # Create Spotify Object
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    # Get Most Recently Liked Song
    song_data = spotify_object.current_user_saved_tracks(limit=1)

    relevant_data = {
        CONST.SONG_NAMES: [],
        CONST.SONG_IDS: [],
        CONST.DURATION: [],
        CONST.SONG_URLS: [],
        CONST.ARTISTS: [],
        CONST.ADDED_AT: []

    }

    # Loop Through All Liked Songs
    while True:

        # Add name and duration to respective lists
        relevant_data = dm.clean_song_data(song_data, relevant_data)

        # Print Progress
        print(relevant_data[CONST.SONG_NAMES][-1], end=" | ")
        print(
            f"{((len(relevant_data[CONST.SONG_NAMES])/song_data[CONST.TOTAL])*100):.2f}%")

        # Iterate to next song/Check if at end
        if song_data[CONST.NEXT]:
            song_data = spotify_object.next(song_data)
        else:
            break
    

    relevant_data = pd.DataFrame.from_dict(relevant_data)

    feature_dict = sft.get_feature_dict(spotianalyze_object, relevant_data)
    feature_dataframe = pd.DataFrame(feature_dict)
    song_dataframe = pd.concat([relevant_data, feature_dataframe], axis=1)
    song_dataframe.to_csv("./data/liked_songs.csv")

    # Output Completed
    return True