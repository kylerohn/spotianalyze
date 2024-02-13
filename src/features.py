from const import CONST
import pandas as pd


####################################################################################################################
# Get Features for Song by ID as Dict from DataFrame


    # Create Spotify Object

    # Get Shape of Dataframe input
    rows, cols = song_dataframe.shape

    # Iterate through Each ID and Append Values to Associated List
    # TODO Make Faster
    for row in range(rows):
        # Get ID of current song in iteration
        current_id = song_dataframe.at[row, CONST.SONG_IDS]

        # Get Response of track features
        track_features = spotify_object.audio_features(current_id)

        # Danceability
        features[CONST.DANCEABILITY].append(
            track_features[0][CONST.DANCEABILITY])

        # Energy
        features[CONST.ENERGY].append(track_features[0][CONST.ENERGY])

        # Key
        features[CONST.KEY].append(track_features[0][CONST.KEY])

        # Loudness
        features[CONST.LOUDNESS].append(track_features[0][CONST.LOUDNESS])

        # Speechiness
        features[CONST.SPEECHINESS].append(
            track_features[0][CONST.SPEECHINESS])

        # Acousticness
        features[CONST.ACOUSTICNESS].append(
            track_features[0][CONST.ACOUSTICNESS])

        # Instrumentalness
        features[CONST.INSTRUMENTALNESS].append(
            track_features[0][CONST.INSTRUMENTALNESS])
            
        # Liveness
        features[CONST.LIVENESS].append(track_features[0][CONST.LIVENESS])

        # Valence
        features[CONST.VALENCE].append(track_features[0][CONST.VALENCE])
        
        # Tempo
        features[CONST.TEMPO].append(track_features[0][CONST.TEMPO])

        print(f"Progress: {(((row + 1)/rows)*100):.2f}%")

    return features
