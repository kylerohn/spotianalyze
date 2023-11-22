import spotianalyze
from playlist import Playlist
from const import CONST
import data_mgr
import playlist_mgr
import numpy as np
import pandas as pd
import library_data as libdata

spotify = spotianalyze.Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445',
                            'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')


wavy = Playlist()


dat_np = data_mgr.numpyify(pd.read_csv(f"data/playlists/{wavy.id}/{wavy.name}.csv"))
attr_val_list = []

c= 1.55

for idx, attr in enumerate(CONST.KEYLIST):
    attr_val_list.append(((np.median(dat_np[:][idx]))-(np.std(dat_np[:][idx])*c), (np.median(dat_np[:][idx])+(np.std(dat_np[:][idx])*c)), attr))

all_songs = pd.read_csv("data/liked_songs.csv")
new_song_list = []

all_songs = all_songs.reset_index()
for index, row in all_songs.iterrows():

    if attr_val_list[0][0] > float(row[CONST.DANCEABILITY]) or attr_val_list[0][1] < float(row[CONST.DANCEABILITY]):
        print(attr_val_list[0][2])
        continue

    if attr_val_list[1][0] > row[CONST.ENERGY] or attr_val_list[1][1] < row[CONST.ENERGY]:
        print(attr_val_list[1][2])
        continue
    
    if attr_val_list[2][0] > row[CONST.KEY] or attr_val_list[2][1] < row[CONST.KEY]:
        print(attr_val_list[2][2])
        continue

    if attr_val_list[3][0] > row[CONST.LOUDNESS] or attr_val_list[3][1] < row[CONST.LOUDNESS]:
        print(attr_val_list[3][2])
        continue

    if attr_val_list[4][0] > row[CONST.SPEECHINESS] or attr_val_list[4][1] < row[CONST.SPEECHINESS]:
        print(attr_val_list[4][2])
        continue

    if attr_val_list[5][0] > row[CONST.ACOUSTICNESS] or attr_val_list[5][1] < row[CONST.ACOUSTICNESS]:
        print(attr_val_list[5][2])
        continue

    if attr_val_list[6][0] > row[CONST.INSTRUMENTALNESS] or attr_val_list[6][1] < row[CONST.INSTRUMENTALNESS]:
        print(attr_val_list[6][2])
        continue

    if attr_val_list[7][0] > row[CONST.LIVENESS] or attr_val_list[7][1] < row[CONST.LIVENESS]:
        print(attr_val_list[7][2])
        continue

    if attr_val_list[8][0] > row[CONST.VALENCE] or attr_val_list[8][1] < row[CONST.VALENCE]:
        print(attr_val_list[8][2])
        continue

    if attr_val_list[9][0] > row[CONST.TEMPO] or attr_val_list[9][1] < row[CONST.TEMPO]:
        print(attr_val_list[9][2])
        continue

    new_song_list.append(row[CONST.SONG_IDS])

print(len(new_song_list))

input()

new_id = playlist_mgr.create_playlist(spotify, f"quintin recs {c}")
playlist_mgr.add_to(spotify, new_id, new_song_list)







# pl_df = pd.read_csv("data/playlists/demon-killer.csv")

# pl_np = dmgr.numpyify(pl_df)

# vis.plt_normal_dist(pl_np)


# liked_songs_df = pd.read_csv("data/liked_songs.csv")
# liked_songs_np = dmgr.numpyify(liked_songs_df[CONST.KEYLIST])

# vis.plt_histogram_by_key(liked_songs_np)

# vis.plt_all_norm(liked_songs_np)
# plt.show()



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