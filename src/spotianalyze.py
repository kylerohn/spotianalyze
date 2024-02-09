
from const import CONST as C
import pandas as pd
from spotipy import Spotify
from re import sub


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
            song_dict = response_transformer(track_info[C.TRACK], song_dict)
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
    pd.DataFrame.from_dict(artist_dict).to_csv(path_or_buf="data/artists.csv")




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
            response_transformer(artist, gp_info)
    
    artist_info_dict[C.GENRES] = gp_info[C.GENRES]
    artist_info_dict[C.POPULARITY] = gp_info[C.POPULARITY]
        

    return new_artist_col, artist_info_dict
    




def response_transformer(response_dict: dict, transformed_reciever: dict):
    for key in transformed_reciever:
        try:
            if key == C.NAME:
                transformed_reciever[key].append(sub("[\(\[].*?[\)\]]","", response_dict[key]))
            else:
                transformed_reciever[key].append(response_dict[key])
            
        except:
            pass
    return transformed_reciever


def divide_list(l, n): 
      
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n]