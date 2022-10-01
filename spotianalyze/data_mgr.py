from const import CONST
import numpy as np
import pandas as pd
from math import pi
from math import e
from math import pow
from math import sqrt


# Create Numpy Array With Given Dictionary Using Pandas
def numpyify(dataframe=pd.DataFrame()):

    rows, cols = dataframe.shape

    data_numpy_sorted = np.empty((rows, len(CONST.KEYLIST)), dtype=float)

    for col, key in enumerate(CONST.KEYLIST):
        for row in range(rows):
            data_numpy_sorted[row, col] = float(dataframe.at[row, key])

    return data_numpy_sorted.transpose()


def clean_song_data(song_data, relevant_data):
    # Local Vars Declaration for Song Info

    # Name
    relevant_data[CONST.SONG_NAMES].append(
        song_data[CONST.ITEMS][0][CONST.TRACK][CONST.NAME])
    # ID
    relevant_data[CONST.SONG_IDS].append(
        song_data[CONST.ITEMS][0][CONST.TRACK][CONST.ID])
    # Duration
    relevant_data[CONST.DURATION].append(
        song_data[CONST.ITEMS][0][CONST.TRACK][CONST.DURATION_MS])
    # Spotify Url
    relevant_data[CONST.SONG_URLS].append(
        song_data[CONST.ITEMS][0][CONST.TRACK][CONST.EXTERNAL_URLS][CONST.SPOTIFY])
    # Added at
    relevant_data[CONST.ADDED_AT].append(
        song_data[CONST.ITEMS][0][CONST.ADDED_AT])
    # Artists
    relevant_data[CONST.ARTISTS].append(
        song_data[CONST.ITEMS][0][CONST.TRACK][CONST.ARTISTS])

    return relevant_data


# Get Songs by Range of Danceibility
def dance_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, danceability in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.DANCEABILITY]):

        if (a <= danceability and danceability <= b):
            final_ids.append(song_id)
            print(song)


# Get Songs by Range of Energy
def energy_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, energy in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.ENERGY]):
        if (a <= energy and energy <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of Loudness
def loudness_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.LOUDNESS]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of Speechiness
def speechiness_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.SPEECHINESS]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of acousticness
def acousticness_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.ACOUSTICNESS]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of Instrumentalness
def instrumentalness_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.INSTRUMENTALNESS]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of Liveness
def liveness_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.LIVENESS]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of Valence
def valence_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.VALENCE]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of Tempo
def tempo_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.TEMPO]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids

# Get Songs by Range of Key
def key_range(a: float, b: float, df_csv="data/liked_songs.csv"):
    liked_df = pd.read_csv(df_csv)
    final_ids = []

    for song, song_id, feature in zip(liked_df[CONST.SONG_NAMES], liked_df[CONST.SONG_IDS], liked_df[CONST.KEY]):
        if (a <= feature and feature <= b):
            final_ids.append(song_id)

    return final_ids


def prob_density(x: np.array, mu: float, sigma: float):
    y = []
    for xn in x:
        y.append((1/sigma * sqrt(2*pi)) * pow(e, (-0.5) * pow((xn-mu)/sigma, 2)))
    y = np.array(y)
    return y