import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil
import spotipy

####################################################################################################################

ALBUM = "album"
ARTIST = "artist"
ARTISTS = "artists"
AVAILABLE_MARKETS = "available_markets"
CONTEXT = "context"
DISC_NUMBER = "disc_number"
DISPLAY_NAME = "display_name"
DURATION = "duration"
DURATION_MS = "duration_ms"
EXPLICIT = "explicit"
EXTERNAL_IDS = "external_ids"
EXTERNAL_URLS = "external_urls"
HREF = "href"
ID = "id"
IS_LOCAL = "is_local"
IS_PLAYING = "is_playing"
ITEM = "item"
ITEMS = "items"
NAME = "name"
NEXT = "next"
OFFSET = "offset"
OWNER = "owner"
PLAYLIST_URI = "playlist_uri"
POPULARITY = "popularity"
PREVIEW_URL = "preview_url"
PROGRESS_MS = "progress_ms"
SONG_INFO = "song_info"
SPOTIFY = "spotify"
TIME_ELAPSED = "time_elapsed"
TIMES_LISTENED = "times_listened"
TIMES_SKIPPED = "times_skipped"
TOTAL = "total"
TRACK = "track"
TRACKS = "tracks"
TRACK_NUMBER = "track_number"
TRACK_URI = "track_uri"
TYPE = "type"
URI = "uri"
URL = "url"

####################################################################################################################

DANCEABILITY = "danceability"
ENERGY = "energy"
KEY = "key"
LOUDNESS = "loudness"
MODE = "mode"
SPEECHINESS = "speechiness"
ACOUSTICNESS = "acousticness"
INSTRUMENTALNESS = "instrumentalness"
LIVENESS = "liveness"
VALENCE = "valence"
TEMPO = "tempo"
TRACK_HREF = "track_href"
ANALYSIS_URL = "analysis_url"
TIME_SIGNATURE = "time_signature"

####################################################################################################################

KEYLIST = [
    DANCEABILITY,
    ENERGY,
    KEY,
    LOUDNESS,
    SPEECHINESS,
    ACOUSTICNESS,
    INSTRUMENTALNESS,
    LIVENESS,
    VALENCE,
    TEMPO,
]
####################################################################################################################
# Data Creation
####################################################################################################################
# Create DataFrame objects of retreived data (Songs/Features and Artists) and save as CSV files
def create_liked_songs_dataframe(spotianalyze_object):

    # Create Spotify Object
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    # Iteration Var
    page = 1

    # Local Vars Declaration for Song Info
    song_names = []
    song_ids = []
    durations_in_ms = []
    song_urls = []
    artists = []

    # Local Vars Declaration for Artist Info
    artist_names = []
    artist_ids = []
    artist_hrefs = []
    artist_urls = []

    # Get Most Recently Liked Song
    current_track = spotify_object.current_user_saved_tracks(limit=1, offset=(page - 1), fields=ITEMS)

    # Loop Through All Liked Songs
    while True:
        # Add name and duration to respective lists
        song_names.append(current_track[ITEMS][0][TRACK][NAME])
        song_ids.append(current_track[ITEMS][0][TRACK][ID])
        durations_in_ms.append(current_track[ITEMS][0][TRACK][DURATION_MS])
        song_urls.append(current_track[ITEMS][0][TRACK][EXTERNAL_URLS][SPOTIFY])
        artist_list = current_track[ITEMS][0][TRACK][ARTISTS]

        # Print Progress
        print(song_names[-1], end=" | ")
        print(f"{((len(song_names)/current_track[TOTAL])*100):.2f}%")

        # Create Dict of Each Artist in Song
        for artist in artist_list:
            # Create List of Values
            values = [
                artist[NAME],
                artist[ID],
                artist[HREF],
                artist[EXTERNAL_URLS][SPOTIFY],
            ]

            # Create List of Keys
            keys = [NAME, ID, HREF, EXTERNAL_URLS]

            # See Dictify
            artist_info = dictify(values, keys)

            # Add to Artist List if Not Added Already
            if artist_info in artists:
                continue
            else:
                artists.append(artist_info)

        # End Loop if End of List
        if not current_track[NEXT]:
            break

        # Iterate to next song
        page += 1
        current_track = spotify_object.current_user_saved_tracks(
            limit=1, offset=(page - 1)
        )

    # Create Dataframe for Artists and Respective Info
    for artist in artists:
        artist_names.append(artist[NAME])
        artist_ids.append(artist[ID])
        artist_hrefs.append(artist[HREF])
        artist_urls.append(artist[EXTERNAL_URLS])
    artist_dataframe = pd.DataFrame(
        {NAME: artist_names, ID: artist_ids, HREF: artist_hrefs, URL: artist_urls}
    )

    # Create CSV file of artist data
    artist_dataframe.to_csv("data/liked_songs_artists.csv")

    # Create Dataframe and CSV file for Songs
    song_dataframe = pd.DataFrame(
        {NAME: song_names, ID: song_ids, DURATION_MS: durations_in_ms, URL: song_urls}
    )

    feature_dict = get_feature_dict(spotianalyze_object, song_dataframe)
    feature_dataframe = pd.DataFrame(feature_dict)
    song_dataframe = pd.concat([song_dataframe, feature_dataframe], axis=1)
    song_dataframe.to_csv("data/liked_songs.csv")

    # Output Completed
    return True

####################################################################################################################
# Create DataFrame objects of given playlist id items
def create_playlist_songs_dataframe(spotianalyze_object, playlist_id):

    # Local Vars Declaration for Song Info
    song_names = []
    song_ids = []
    durations_in_ms = []
    song_urls = []

    # Create Spotify Object
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    # Create Playlist Object
    playlist_data = spotify_object.playlist(playlist_id)
    current_track = playlist_data[TRACKS]
    name = playlist_data[NAME]
    while True:
        for idx, song in enumerate(current_track[ITEMS]):
            # Add name and duration to respective lists
            song_names.append(song[TRACK][NAME])
            song_ids.append(song[TRACK][ID])
            durations_in_ms.append(song[TRACK][DURATION_MS])
            song_urls.append(song[TRACK][EXTERNAL_URLS][SPOTIFY])
            print(song_names[idx])

            # Pretty Print
            print(f"{(idx + 1) + (current_track[OFFSET])}: {song[TRACK][NAME]} | {((len(song_names)/current_track[TOTAL])*100):.2f}%")

        # Check for Next Page
        if current_track[NEXT]:
            current_track = spotify_object.next(current_track)
        else:
            break

    # Create Dataframe and CSV file for Songs
    song_dataframe = pd.DataFrame(
        {NAME: song_names, ID: song_ids, DURATION_MS: durations_in_ms, URL: song_urls}
    )

    feature_dict = get_feature_dict(spotianalyze_object, song_dataframe)
    feature_dataframe = pd.DataFrame(feature_dict)
    song_dataframe = pd.concat([song_dataframe, feature_dataframe], axis=1)
    song_dataframe.to_csv(f"data/{name}.csv")

    # Output Completed
    return True

####################################################################################################################
# Get Features for Song by ID as Dict from DataFrame
def get_feature_dict(spotianalyze_object, song_dataframe=pd.DataFrame()):

    # Local Vars Declaration for Song Features
    danceability = []
    energy = []
    key = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []

    # Create Spotify Object
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    # Get Shape of Dataframe input
    rows, cols = song_dataframe.shape

    # Iterate through Each ID and Append Values to Associated List
    for row in range(rows):
        current_id = song_dataframe.at[row, ID]
        track_features = spotify_object.audio_features(current_id)
        danceability.append(track_features[0][DANCEABILITY])
        energy.append(track_features[0][ENERGY])
        key.append(track_features[0][KEY])
        loudness.append(track_features[0][LOUDNESS])
        speechiness.append(track_features[0][SPEECHINESS])
        acousticness.append(track_features[0][ACOUSTICNESS])
        instrumentalness.append(track_features[0][INSTRUMENTALNESS])
        liveness.append(track_features[0][LIVENESS])
        valence.append(track_features[0][VALENCE])
        tempo.append(track_features[0][TEMPO])

        print(f"Progress: {(((row + 1)/rows)*100):.2f}%")

    feature_dict = {
        DANCEABILITY: danceability,
        ENERGY: energy,
        KEY: key,
        LOUDNESS: loudness,
        SPEECHINESS: speechiness,
        ACOUSTICNESS: acousticness,
        INSTRUMENTALNESS: instrumentalness,
        LIVENESS: liveness,
        VALENCE: valence,
        TEMPO: tempo,
        TIMES_LISTENED: 0,
        TIMES_SKIPPED: 0,
    }

    return feature_dict


####################################################################################################################
# Creates Dictionary with list of values, and list of key value pairs
def dictify(values: list(), keys: list()):

    dictionary = {}
    if len(values) != len(keys):
        return -1

    for idx, key in enumerate(keys):
        dictionary[key] = values[idx]

    return dictionary


####################################################################################################################
# Real Time Data
####################################################################################################################
# Get Data of the Currently Playing Song
def get_currently_playing_data(spotianalyze_object):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    playlist_uri = None

    raw_json = spotify_object.current_user_playing_track()

    name = raw_json[ITEM][NAME]
    artists = raw_json[ITEM][ARTISTS]
    duration = raw_json[ITEM][DURATION_MS]
    track_id = raw_json[ITEM][ID]

    context = raw_json[CONTEXT][TYPE]
    if context == "playlist":
        playlist_uri = raw_json[CONTEXT][URI]
    progress = raw_json[PROGRESS_MS]
    is_playing = raw_json[IS_PLAYING]

    track_features = spotify_object.audio_features(track_id)

    current_playing_data = {
        NAME: name,
        ARTISTS: artists,
        DURATION_MS: duration,
        ID: track_id,
        CONTEXT: context,
        PROGRESS_MS: progress,
        IS_PLAYING: is_playing,
        PLAYLIST_URI: playlist_uri,
        DANCEABILITY: track_features[0][DANCEABILITY],
        ENERGY: track_features[0][ENERGY],
        KEY: track_features[0][KEY],
        LOUDNESS: track_features[0][LOUDNESS],
        SPEECHINESS: track_features[0][SPEECHINESS],
        INSTRUMENTALNESS: track_features[0][INSTRUMENTALNESS],
        ACOUSTICNESS: track_features[0][ACOUSTICNESS],
        LIVENESS: track_features[0][LIVENESS],
        VALENCE: track_features[0][VALENCE],
        TEMPO: track_features[0][TEMPO],
    }

    return current_playing_data


####################################################################################################################
# TODO Data Manipulation/Visualizaton
####################################################################################################################
# Create Numpy Array With Given Dictionary Using Pandas
def numpyify(dataframe=pd.DataFrame()):

    rows, cols = dataframe.shape

    data_numpy_sorted = np.empty((rows, len(KEYLIST)), dtype=float)

    for col, key in enumerate(KEYLIST):
        for row in range(rows):
            data_numpy_sorted[row, col] = float(dataframe.at[row, key])

    return data_numpy_sorted


####################################################################################################################
# Create MATPLOTLIB Graphs of Data Given np matrix
def plt_histogram_by_key(numpy_matrix):

    for idx, k in enumerate(KEYLIST):
        plt.hist(numpy_matrix.transpose()[:][idx], snap=True)
        plt.gca().set(title=k, ylabel="Frequency")
        plt.show()



####################################################################################################################
# TODO Playlist Stuff
####################################################################################################################
# User Playlist Search/Selection
def user_playlist_search(spotianalyze_object):

    # Local Var Declaration for List of User Created Playlist
    playlist_list = []

    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    current_user = spotify_object.current_user()
    playlists = spotify_object.current_user_playlists()
    for idx, playlist in enumerate(playlists[ITEMS]):
        if playlists[ITEMS][idx][OWNER][DISPLAY_NAME] == current_user[DISPLAY_NAME]:
            playlist_list.append(playlist)

    for idx, playlist in enumerate(playlist_list):
        print(f"{idx + 1}: {playlist[NAME]}")

    print("Type the Playlist Number You Want to Analyze: ", end=" ")
    idx = int(input())
    return (playlist_list[idx - 1][ID])







# !ONLY COMPLETE UNTIL HERE
####################################################################################################################

# TODO Playlist Search by Keyword
# TODO Add Song to User Playlist
# TODO Remove Song from User Playlist

###################################################################################################################
# Library Manipulation
####################################################################################################################
# TODO Add song to Library

####################################################################################################################
# TODO Remove song from library

####################################################################################################################
# Get Spotify Song Attributes
####################################################################################################################
# !GOD FIX ALL OF THIS FUCK
# Get Danceability by Range of Numbers
def danceability_range(csvfile, start=0.0, stop=1.0):
    with open(csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[2] == DANCEABILITY:
                continue
            elif (start < float(row[2])) and (stop > float(row[2])):
                print(row)


####################################################################################################################
# Get Energy by Range of Numbers
def energy_range(csvfile, start=0.0, stop=1.0):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[3] == ENERGY:
                continue
            elif (start < float(row[3])) and (stop > float(row[3])):
                print(row)


####################################################################################################################
# Get Key by Range of Numbers
def key_range(csvfile, start=0, stop=11):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[4] == KEY:
                continue
            elif (start <= float(row[4])) and (stop >= float(row[4])):
                print(row)


####################################################################################################################
# Get Loudness by Range of Numbers
def loudness_range(csvfile: str, start=-20.0, stop=0.0):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[5] == LOUDNESS:
                continue
            elif (start <= float(row[5])) and (stop >= float(row[5])):
                print(row)


####################################################################################################################
# Get Speechiness by Range of Numbers
def speehiness_range(csvfile: str, start=0.0, stop=1.0):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[7] == SPEECHINESS:
                continue
            elif (start <= float(row[7])) and (stop >= float(row[7])):
                print(row)


####################################################################################################################
# Get Acousticness by Range of Numbers
def acousticness_range(csvfile: str, start=0.0, stop=1.0):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[8] == ACOUSTICNESS:
                continue
            elif (start <= float(row[8])) and (stop >= float(row[8])):
                print(row)


####################################################################################################################
# Get Instrumentalness by Range of Numbers
def instrumentalness_range(csvfile: str, start=0.0, stop=1.0):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[9] == INSTRUMENTALNESS:
                continue
            elif (start <= float(row[9])) and (stop >= float(row[9])):
                print(row)


####################################################################################################################
#  Get Liveness by Range of Numbers
def liveness_range(csvfile: str, start=0.0, stop=1.0):
    with open("da/" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[10] == LIVENESS:
                continue
            elif (start <= float(row[10])) and (stop >= float(row[10])):
                print(row)


####################################################################################################################
# Get Valence by Range of Numbers
def valence_range(csvfile: str, start=0.0, stop=1.0):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[11] == VALENCE:
                continue
            elif (start <= float(row[11])) and (stop >= float(row[11])):
                print(row)


####################################################################################################################
# Get Tempo by Range of Numbers
def tempo_range(csvfile: str, start=0.0, stop=250.0):
    with open("" + csvfile, "r") as infile:
        rows_songs = csv.reader(infile)
        for row in rows_songs:
            if row[12] == TEMPO:
                continue
            elif (start <= float(row[12])) and (stop >= float(row[12])):
                print(row)


