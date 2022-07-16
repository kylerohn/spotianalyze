import csv
import pandas as pd
import psutil
import spotipy
import numpy as np
import matplotlib.pyplot as plt

####################################################################################################################

ALBUM = "album"
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
OWNER = "owner"
POPULARITY = "popularity"
PREVIEW_URL = "preview_url"
PROGRESS_MS = "progress_ms"
SONG_INFO = "song_info"
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
# Create list of all songs in library
def get_library_song_list(spotianalyze_object):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    song_list = []
    page = 1
    while (
        len(
            spotify_object.current_user_saved_tracks(
                limit=1, offset=(page - 1)
            )["items"]
        )
        != 0
    ):
        temp_song_list = spotianalyze_object.SPOTIFY_OBJECT.current_user_saved_tracks(
            limit=1, offset=(page - 1)
        )["items"]
        song_list = song_list + temp_song_list
        page = page + 1

    song_list


####################################################################################################################
# Create list of dicts for each song and associated data
# TODO Pandasify
def create_song_list_dict(spotianalyze_object, song_list):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    it = 1
    full_song_data = []

    for track in song_list:
        # Display Progress
        print(f"{(it/len(song_list)) * 100}%", end=" ")
        print("RAM memory % used:", psutil.virtual_memory()[2])

        # Iteration Reqs
        it = it + 1
        track_uri = track[TRACK][ID]
        track_features = spotianalyze_object.SPOTIFY_OBJECT.audio_features(track_uri)
        # Dict Creation
        full_dict = {
            NAME: track[TRACK][NAME],
            ARTISTS: track[TRACK][ARTISTS],
            ID: track_uri,
            DURATION_MS: track[TRACK][DURATION_MS],
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
            TIME_SIGNATURE: track_features[0][TIME_SIGNATURE],
            TIMES_LISTENED: 0,
            TIMES_SKIPPED: 0,
        }
        full_song_data.append(full_dict)
    print(len(full_song_data))
    return full_song_data


####################################################################################################################
# Real Time Data
####################################################################################################################
# Get Data of the Currently Playing Song
def get_currently_playing_data(spotianalyze_object):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    name = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[ITEM][NAME]
    artists = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[ITEM][
        ARTISTS
    ]
    duration = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[ITEM][
        DURATION_MS
    ]
    track_id = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[ITEM][ID]

    context = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[CONTEXT][
        TYPE
    ]
    if context == "playlist":
        playlist_uri = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[
            CONTEXT
        ][URI]
    progress = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[
        PROGRESS_MS
    ]
    is_playing = spotianalyze_object.SPOTIFY_OBJECT.current_user_playing_track()[
        IS_PLAYING
    ]

    track_features = spotianalyze_object.SPOTIFY_OBJECT.audio_features(track_id)

    current_playing_data = {
        NAME: name,
        ARTISTS: artists,
        DURATION_MS: duration,
        ID: track_id,
        CONTEXT: context,
        PROGRESS_MS: progress,
        IS_PLAYING: is_playing,
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
# TODO Playlist Stuff
####################################################################################################################
# User Playlist Search/Selection
def user_playlist_search(spotianalyze_object):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    current_user = spotianalyze_object.SPOTIFY_OBJECT.current_user()
    playlists = spotianalyze_object.SPOTIFY_OBJECT.current_user_playlists()
    for idx, playlist in enumerate(playlists[ITEMS]):
        if playlists[ITEMS][idx][OWNER][DISPLAY_NAME] == current_user[DISPLAY_NAME]:
            print(f"{idx + 1}: {playlist[NAME]}")

    print("Type the Playlist Number You Want to Analyze: ", end=" ")
    idx = int(input())
    return playlists[ITEMS][idx - 1][ID]


####################################################################################################################
# TODO User Playlist Data Collection Pandasfied
def get_playlist_info_dict(spotianalyze_object, playlist_id):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    playlist_items_dict = {}
    playlist_items_list = []
    playlist_items = spotianalyze_object.SPOTIFY_OBJECT.playlist_items(
        playlist_id, limit=20
    )
    for song in playlist_items[ITEMS]:
        track_features = spotianalyze_object.SPOTIFY_OBJECT.audio_features(
            song[TRACK][ID]
        )
        playlist_items_dict = {
            NAME: song[TRACK][NAME],
            ARTISTS: song[TRACK][ARTISTS],
            DURATION_MS: song[TRACK][DURATION_MS],
            ID: song[TRACK][ID],
            IS_LOCAL: song[IS_LOCAL],
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
        playlist_items_list.append(playlist_items_dict)

    while playlist_items[NEXT]:
        playlist_items = spotianalyze_object.SPOTIFY_OBJECT.next(playlist_items)
        for song in playlist_items[ITEMS]:
            track_features = spotianalyze_object.SPOTIFY_OBJECT.audio_features(
                song[TRACK][ID]
            )
            playlist_items_dict = {
                NAME: song[TRACK][NAME],
                ARTISTS: song[TRACK][ARTISTS],
                DURATION_MS: song[TRACK][DURATION_MS],
                ID: song[TRACK][ID],
                IS_LOCAL: song[IS_LOCAL],
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
            playlist_items_list.append(playlist_items_dict)
    return playlist_items_list


# TODO Create Playlist csv file -- PANDAS
def create_playlist_csv(spotianalyze_object, playlist_id, playlist_item_list):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    current_user = spotianalyze_object.SPOTIFY_OBJECT.current_user()
    playlists = spotianalyze_object.SPOTIFY_OBJECT.current_user_playlists()
    for playlist in playlists[ITEMS]:
        print(playlist[ID])
        print(playlist_id)
        if (playlist[ID] == playlist_id) and (
            playlist[OWNER][DISPLAY_NAME] == current_user[DISPLAY_NAME]
        ):
            filename = playlist[NAME]
            write_csv(playlist_item_list, filename[0:4] + ".csv")
            return True
        else:
            continue

    return False


# TODO Playlist Search by Keyword
# TODO Add Song to User Playlist
# TODO Remove Song from User Playlist


####################################################################################################################
# TODO Numpy Shenanigans ...with pandas...
####################################################################################################################
# TODO Create Numpy Array With Given Dictionary Using Pandas
def numpify(csvfile: str):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    song_info = read_csv(csvfile)
    feature_array = np.zeros((len(KEYLIST), len(song_info)))
    for idx1, key in enumerate(KEYLIST):
        for idx2, song_feature_items in enumerate(song_info):
            feature_array[idx1][idx2] = song_feature_items[key]

    return feature_array


###################################################################################################################
# Library Manipulation
####################################################################################################################
# Add song to Library
# TODO Make Work With Multiple Songs
def add_song_to_library(spotianalyze_object, current_playing_data, csvfile):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    spotianalyze_object.SPOTIFY_OBJECT.current_user_saved_tracks_add(
        current_playing_data[ID]
    )
    old_data = read_csv(csvfile)
    additional_data = [
        {
            NAME: current_playing_data[NAME],
            ARTISTS: current_playing_data[ARTISTS],
            ID: current_playing_data[ID],
            DANCEABILITY: current_playing_data[DANCEABILITY],
            ENERGY: current_playing_data[ENERGY],
            KEY: current_playing_data[KEY],
            LOUDNESS: current_playing_data[LOUDNESS],
            SPEECHINESS: current_playing_data[SPEECHINESS],
            INSTRUMENTALNESS: current_playing_data[INSTRUMENTALNESS],
            ACOUSTICNESS: current_playing_data[ACOUSTICNESS],
            LIVENESS: current_playing_data[LIVENESS],
            VALENCE: current_playing_data[VALENCE],
            TEMPO: current_playing_data[TEMPO],
        }
    ]

    write_csv(additional_data + old_data)


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


# TODO Create MATPLOTLIB Graphs of Data Given Dictionaries


def matplotlib_scatter_by_key(numpy_matrix):
    for idx, k in enumerate(KEYLIST):
        plt.hist(numpy_matrix[:][idx], bins=100)
        plt.gca().set(title=k, ylabel="Frequency")
        plt.show()
