from const import CONST
import features as sft
import pandas as pd

####################################################################################################################
# User Playlist Search/Selection
def user_playlist_search(spotianalyze_object):
    '''
    Search for playlists owned by user to make a selection
    '''

    # Local Var Declaration for List of User Created Playlist
    playlist_list = []

    spotify_object = spotianalyze_object.SPOTIFY_OBJECT
    current_user = spotify_object.current_user()
    playlists = spotify_object.current_user_playlists()
    for idx, playlist in enumerate(playlists[CONST.ITEMS]):
        # if playlists[CONST.ITEMS][idx][CONST.OWNER][CONST.DISPLAY_NAME] == current_user[CONST.DISPLAY_NAME]:
        playlist_list.append(playlist)

    for idx, playlist in enumerate(playlist_list):
        print(f"{idx + 1}: {playlist[CONST.NAME]}")

    print("Type the Playlist Number You Want to Analyze: ", end=" ")
    idx = int(input())
    return playlist_list[idx - 1][CONST.ID], playlist_list[idx - 1][CONST.NAME]

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
    current_track = playlist_data[CONST.TRACKS]
    name = playlist_data[CONST.NAME]
    while True:
        for idx, song in enumerate(current_track[CONST.ITEMS]):
            # Add name and duration to respective lists
            song_names.append(song[CONST.TRACK][CONST.NAME])
            song_ids.append(song[CONST.TRACK][CONST.ID])
            durations_in_ms.append(song[CONST.TRACK][CONST.DURATION_MS])
            song_urls.append(song[CONST.TRACK]
                             [CONST.EXTERNAL_URLS][CONST.SPOTIFY])

            # Pretty Print
            print(
                f"{(idx + 1) + (current_track[CONST.OFFSET])}: {song[CONST.TRACK][CONST.NAME]} | {((len(song_names)/current_track[CONST.TOTAL])*100):.2f}%"
            )

        # Check for Next Page
        if current_track[CONST.NEXT]:
            current_track = spotify_object.next(current_track)
        else:
            break

    # Create Dataframe and CSV file for Songs
    song_dataframe = pd.DataFrame(
        {CONST.NAME: song_names, CONST.SONG_IDS: song_ids,
            CONST.DURATION_MS: durations_in_ms, CONST.URL: song_urls}
    )

    feature_dict = sft.get_feature_dict(spotianalyze_object, song_dataframe)
    feature_dataframe = pd.DataFrame(feature_dict)
    song_dataframe = pd.concat([song_dataframe, feature_dataframe], axis=1)
    song_dataframe.to_csv(f"data/playlists/{playlist_id}/{name}.csv")

    # Output Completed
    return True
