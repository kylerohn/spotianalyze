
from const import CONST as C
import pandas as pd
from spotipy import Spotify
from re import sub
import numpy as np
import matplotlib.pyplot as plt


# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def create_library(spotify_object: Spotify):
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

    # Initialize a dictionary to store information about the user's liked songs
    song_dict = {
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
            song_dict = _response_transformer(track_info[C.TRACK], song_dict)
            print(song_dict[C.NAME][-1])

        # Print the names of the tracks (for demonstration purposes)

        # Check if there are more pages
        if not saved_tracks['next']:
            next_page = False
        else:
            # Move to the next page of saved tracks
            saved_tracks = spotify_object.next(saved_tracks)
    
    # artist information processing
    artist_uris, artist_dict = _artist_parser(spotify_object, song_dict[C.ARTISTS])

    del song_dict[C.ARTISTS]
    song_dict[C.ARTISTS] = artist_uris


    # Return a dataframe containing information about the user's liked songs
    pd.DataFrame.from_dict(song_dict).to_csv(path_or_buf="data/library.csv")

    artist_data = pd.DataFrame.from_dict(artist_dict)
    artist_data.drop_duplicates(subset=[C.ARTISTS], inplace=True)
    artist_data.to_csv(path_or_buf="data/artists.csv", index=False)
    add_feature_dict(spotify_object, "data/library.csv")

# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def create_from_playlist(spotify_object: Spotify):


# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
    
def add_feature_dict(spotify_object, song_csv: str):

    # Local Vars Declaration for Song Features
    features = {
        C.DANCEABILITY: [],
        C.ENERGY: [],
        C.KEY: [],
        C.LOUDNESS: [],
        C.SPEECHINESS: [],
        C.ACOUSTICNESS: [],
        C.INSTRUMENTALNESS: [],
        C.LIVENESS: [],
        C.VALENCE: [],
        C.TEMPO: []
    }


    song_data = pd.read_csv(filepath_or_buffer=song_csv)
    uri_list = song_data[C.URI].to_list()
    uri_segments = list(divide_list(uri_list, 100))

    for uri_range in uri_segments:
        feature_range = spotify_object.audio_features(tracks=uri_range)

        
        for feature in feature_range:
            _response_transformer(feature, features)
    
    feature_data = pd.DataFrame.from_dict(features)
    song_data = pd.merge(song_data, feature_data, left_index=True, right_index=True)
    song_data.to_csv(song_csv, index=False)

# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def _artist_parser(spotify_object: Spotify, artists: dict):
    """
    Parses the artist information from the Spotify API Library response and updates the complete dictionary.

    Args:
        spotify_object (Spotify): An instance of the Spotify API Library object.
        complete_dict (dict): The complete dictionary containing all parsed information.

    Returns:
        dict: The updated complete dictionary with artist information.

    Note:
        This function modifies the 'complete_dict' in-place and does not return a new dictionary.

    """
        # Initialize a dictionary to store artist information
    
    new_artist_col = []

    artist_info_dict = {C.ARTISTS: [],
                        C.GENRES: [],
                        C.POPULARITY:[],
                        C.URI: []}
    
    gp_info = {C.GENRES: [],
               C.POPULARITY: []}

    # Iterate through the list of artists in the complete dictionary
    for idx, _artists in enumerate(artists):

        new_artist_row = []

        for artist in _artists:
            print(artist[C.NAME])
            new_artist_row.append(artist[C.URI])
            if artist in artist_info_dict[C.ARTISTS]:
                pass
            artist_info_dict[C.ARTISTS].append(artist[C.NAME])
            artist_info_dict[C.URI].append(artist[C.URI])

        new_artist_col.append(new_artist_row)
    
    uri_segments = list(divide_list(artist_info_dict[C.URI], 50))

    for uri_range in uri_segments:
        artist_range = spotify_object.artists(uri_range)
        for artist in artist_range[C.ARTISTS]:
            _response_transformer(artist, gp_info)
    
    artist_info_dict[C.GENRES] = gp_info[C.GENRES]
    artist_info_dict[C.POPULARITY] = gp_info[C.POPULARITY]

    return new_artist_col, artist_info_dict
    
# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def _response_transformer(response_dict: dict, transformed_reciever: dict):
    for key in transformed_reciever:
        try:
            if key == C.NAME:
                transformed_reciever[key].append(sub("[\(\[].*?[\)\]]","", response_dict[key]))
            else:
                transformed_reciever[key].append(response_dict[key])
            
        except:
            pass
    return transformed_reciever

# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def divide_list(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n]

# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def features_histogram(library_filepath: str):
    
    A = get_features_matrix(library_filepath)

    fig, axs = plt.subplots(2, 5)

    axs = np.reshape(axs, newshape=(1, 10))

    for i, ax in enumerate(axs[0]):
        ax.hist(A[i])
        ax.set_title(C.KEYLIST[i])

    axs = np.reshape(axs, newshape=(2, 5))
    plt.show()

# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def get_features_matrix(library_filepath):
    song_data = pd.read_csv(filepath_or_buffer=library_filepath)
    A = []
    for key in C.KEYLIST:
        data = song_data[key].to_numpy()
        A.append(data)
    A = np.array(A)
    return A