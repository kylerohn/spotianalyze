import spotianalyze as s
import os
import pandas as pd
import data_mgr as dmr
from const import CONST
import playlist_data as pldata


class Playlist():

    # Init
    def __init__(self, playlist_id=None):

        self.spotify_object = s.Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445',
                                             'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')

        if playlist_id == None:
            playlist_id, name = pldata.user_playlist_search(
                self.spotify_object)
        else:
            raw_pldata = self.spotify_object.playlist(playlist_id)
            name = raw_pldata[CONST.NAME]

        self.id = playlist_id
        self.name = name

        dirs = os.listdir('data/playlists')
        if playlist_id not in dirs:
            os.mkdir("data/playlists/" + playlist_id)
            pldata.create_playlist_songs_dataframe(
                self.spotify_object, playlist_id)

        lib_data = pd.read_csv("data/liked_songs.csv")
        playlist_data = pd.read_csv(
            "data/playlists/" + self.id + "/" + self.name + ".csv")

        lib_idx_list = []

        dirs = os.listdir('data/playlists/' + self.id)
        if CONST.CLEANSED not in dirs:
            for lib_idx, lib_song_id in enumerate(lib_data[CONST.SONG_IDS]):
                for play_idx, play_song_id in enumerate(playlist_data[CONST.SONG_IDS]):
                    if lib_song_id == play_song_id:
                        lib_idx_list.append(lib_idx)
            cleansed_data = (lib_data.iloc[lib_idx_list, :])
            cleansed_data.to_csv(f"data/playlists/{self.id}/cleansed.csv")

    def __repr__(self) -> str:
        return self.name

    def dat(self):
        self.data = pd.read_csv(f"data/playlists/{self.id}/cleansed.csv")
        return self.data
