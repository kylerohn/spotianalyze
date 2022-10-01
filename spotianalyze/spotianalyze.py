import vis
import data_mgr as dmgr
from const import CONST
import playlist_mgr as pmgr
import os
import spotipy
import spotipy.util as util
from sklearn.cluster import KMeans
from json.decoder import JSONDecodeError
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



class Spotianalyze:
    ##################################################################################################################################

    # Welcome to Spotianalyze

    ##################################################################################################################################
    # Initialize User
    def __init__(self, username: str, client_id: str, client_secret: str, redirect_uri: str):
        '''
        Authentication for Spotify API
        '''

        self.USERNAME = username
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIERECT_URI = redirect_uri

        os.environ['SPOTIPY_CLIENT_ID'] = client_id
        os.environ['SPOTIPY_CLIENT_SECRET'] = client_secret
        os.environ['SPOTIPY_REDIRECT_URI'] = redirect_uri

        scope = 'user-read-private user-read-playback-state playlist-modify-public user-library-modify user-library-read playlist-read-private playlist-modify-private'
        try:
            token = util.prompt_for_user_token(username, scope)
        except (AttributeError, JSONDecodeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope)
        spotify_object = spotipy.Spotify(auth=token)
        user = spotify_object.current_user()
        self.SPOTIFY_OBJECT = spotify_object

    def __repr__(self):
        return self.SPOTIFY_OBJECT

##################################################################################################################################


spotianalyze = Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445',
                            'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')


liked_songs_df = pd.read_csv("data/liked_songs.csv")

liked_songs_np = dmgr.numpyify(liked_songs_df[CONST.KEYLIST])

# vis.plt_histogram_by_key(liked_songs_np)

vis.plt_all_norm(liked_songs_np)
plt.show()



# Weird Shit
# key_tempo_energy = np.array([liked_songs_np[2, :], liked_songs_np[-1, :], liked_songs_np[1, :]])
# # key_tempo_energy = key_tempo_energy.transpose()
# # print(key_tempo_energy)
# # Plot (Key, Tempo, Energy)
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# ax.scatter(key_tempo_energy[:, 0], key_tempo_energy[:, 1], key_tempo_energy[:, 2])
# plt.show()

# K-Means Clusering
# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# scaler = StandardScaler()
# scaled_df_kmeans = scaler.fit_transform(key_tempo_energy)
# kmeans_model = KMeans(n_clusters=3)
# clusters = kmeans_model.fit_predict(key_tempo_energy)
# fig = plt.figure()
# ax = fig.add_subplot(projection='3d')
# for idx, cluster in enumerate(clusters):
#     if cluster == 0:
#         ax.scatter(key_tempo_energy[idx, 0], key_tempo_energy[idx, -1], key_tempo_energy[idx, 1], c='r')
# for idx, cluster in enumerate(clusters):
#     if cluster == 1:
#         ax.scatter(key_tempo_energy[idx, 0], key_tempo_energy[idx, -1], key_tempo_energy[idx, 1], c='g')
# for idx, cluster in enumerate(clusters):
#     if cluster == 2:
#         ax.scatter(key_tempo_energy[idx, 0], key_tempo_energy[idx, -1], key_tempo_energy[idx, 1], c='b')
# plt.show()

# K-Means Cluserting other stuff
# ssd = []
# for k in range(2, 9):
#     kmeans_model = KMeans(n_clusters=k)
#     kmeans_model.fit(key_tempo_energy)
#     ssd.append(kmeans_model.inertia_)
# plt.figure(figsize=(6, 4), dpi=100)
# plt.plot(range(2, 9), ssd, color="green", marker="o")
# plt.xlabel("Number of clusters (K)")
# plt.ylabel("SSD for K")
# plt.show()
