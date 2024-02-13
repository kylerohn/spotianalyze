
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
    """
    Creates a CSV file containing songs from a selected playlist on Spotify.

    Args:
        spotify_object (Spotify): An authenticated instance of the Spotify API.

    Returns:
        None
    """
    # Initialize a dictionary to store song information
    song_dict = {
        C.ARTISTS: [],
        C.DURATION_MS: [],
        C.EXPLICIT: [],
        C.NAME: [],
        C.POPULARITY: [],
        C.URI: []
    }

    # Initialize empty lists to store URIs and names of playlists
    uris = []
    names = []

    # Iterate through user playlists to find the selected playlist
    for item in spotify_object.current_user_playlists()[C.ITEMS]:
        # Check if the playlist belongs to the user
        if item[C.OWNER][C.DISPLAY_NAME] == C.USER:
            uris.append(item[C.URI])
            names.append(item[C.NAME])
            # Print playlist names for user selection
            print(f"{len(uris)}: {item[C.NAME]}")

    # Prompt user to select a playlist
    selection = int(input("> ")) - 1

    # Set limit for number of tracks to fetch per API request
    limit = 100

    # Flag to control pagination
    next_page = True

    # Fetch playlist tracks
    playlist_tracks = spotify_object.playlist_items(uris[selection], limit=limit)

    while next_page:
        # Extract information about the tracks from the current set
        playlist_tracks_info = playlist_tracks[C.ITEMS]

        # Extract and store relevant data in the dictionary
        for track_info in playlist_tracks_info:
            song_dict = _response_transformer(track_info[C.TRACK], song_dict)
            print(song_dict[C.NAME][-1])

        # Check if there are more pages
        if not playlist_tracks['next']:
            next_page = False
        else:
            # Move to the next page of playlist tracks
            playlist_tracks = spotify_object.next(playlist_tracks)

    # Parse artist information and update song dictionary
    artist_uris, artist_dict = _artist_parser(spotify_object, song_dict[C.ARTISTS])
    del song_dict[C.ARTISTS]
    song_dict[C.ARTISTS] = artist_uris

    # Convert song dictionary to DataFrame and save as CSV file
    pd.DataFrame.from_dict(song_dict).to_csv(path_or_buf=f"data/{names[selection]}.csv")

    # Add features to the CSV file
    add_feature_dict(spotify_object, f"data/{names[selection]}.csv")

# =========================================================================================================
# =========================================================================================================
# =========================================================================================================
    
def add_feature_dict(spotify_object, song_csv: str):
    """
    Fetches audio features for songs in a CSV file and adds them to the file.

    Args:
        spotify_object: An authenticated instance of the Spotify API.
        song_csv (str): Path to the CSV file containing song data.

    Returns:
        None
    """
    # Initialize a dictionary to store song features
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

    # Read song data from CSV file
    song_data = pd.read_csv(filepath_or_buffer=song_csv)

    # Extract URIs from the song data
    uri_list = song_data[C.URI].to_list()

    # Divide URIs into segments to handle API limitations
    uri_segments = list(divide_list(uri_list, 100))

    # Fetch audio features for each segment of URIs
    for uri_range in uri_segments:
        feature_range = spotify_object.audio_features(tracks=uri_range)

        # Extract and store audio features in the dictionary
        for feature in feature_range:
            _response_transformer(feature, features)

    # Convert feature dictionary to DataFrame
    feature_data = pd.DataFrame.from_dict(features)

    # Merge feature data with song data based on index
    song_data = pd.merge(song_data, feature_data, left_index=True, right_index=True)

    # Save the updated song data to the CSV file
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

def _response_transformer(response_dict: dict, transformed_receiver: dict):
    """
    Transforms a dictionary response into a format suitable for storage.

    Args:
        response_dict (dict): The dictionary containing the response data.
        transformed_receiver (dict): The dictionary to which the transformed data will be appended.

    Returns:
        dict: The transformed receiver dictionary.
    """
    # Iterate over each key in the transformed receiver dictionary
    for key in transformed_receiver:
        try:
            # Check if the key is "name" to remove any extra information
            if key == C.NAME:
                transformed_receiver[key].append(sub("[\(\[].*?[\)\]]", "", response_dict[key]))
            else:
                transformed_receiver[key].append(response_dict[key])
        except:
            pass  # Skip any errors that occur during transformation

    return transformed_receiver


# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def divide_list(l, n):
    """
    Divides a list into chunks of size n.

    Args:
        l (list): The list to be divided.
        n (int): The size of each chunk.

    Yields:
        list: A chunk of the original list.
    """
    # Loop through the list in steps of size n
    for i in range(0, len(l), n):
        # Yield a chunk of the list containing n elements
        yield l[i:i + n]


# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def features_histogram(library_filepath: str):
    """
    Plots histograms for each feature in a features matrix.

    Args:
        library_filepath (str): Path to the library file containing features matrix.

    Returns:
        None
    """
    # Get the features matrix
    A = get_features_matrix(library_filepath)

    # Create subplots for each feature
    fig, axs = plt.subplots(2, 5)

    # Reshape the axs array for easier iteration
    axs = np.reshape(axs, newshape=(1, 10))

    # Iterate over each subplot and plot histogram for the corresponding feature
    for i, ax in enumerate(axs[0]):
        ax.hist(A[i])
        ax.set_title(C.KEYLIST[i])  # Set the title of the subplot to the feature name

    # Reshape the axs array back to its original shape
    axs = np.reshape(axs, newshape=(2, 5))

    # Display the plot
    plt.show()


# =========================================================================================================
# =========================================================================================================
# =========================================================================================================

def get_features_matrix(library_filepath):
    """
    Reads song data from a CSV file and creates a features matrix.

    Args:
        library_filepath (str): Path to the library file containing song data.

    Returns:
        numpy.ndarray: Features matrix where each row represents a feature array.
    """
    # Read song data from the CSV file
    song_data = pd.read_csv(filepath_or_buffer=library_filepath)

    # Initialize an empty list to store feature arrays
    A = []

    # Iterate over each feature in the KEYLIST
    for key in C.KEYLIST:
        # Extract the feature data as a numpy array
        data = song_data[key].to_numpy()
        
        # Append the feature array to the features matrix
        A.append(data)
    
    # Convert the list of feature arrays into a numpy array
    A = np.array(A)
    
    return A
