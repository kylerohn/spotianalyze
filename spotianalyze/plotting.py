from spotianalyze import Spotianalyze
import playlist_data as ply_dat
import data_mgr as dmr
import pandas as pd
import vis




spotify = Spotianalyze('kyler4646', '4fd6158dd6e34661a9189a2cb2122445',
                            'ee472e4cf73743009fec5d6fb827a8c1', 'https://google.com/')

ply_id, name = ply_dat.user_playlist_search(spotify)

dat_np = dmr.numpyify(pd.read_csv(f"data/playlists/{ply_id}/{name}.csv"))

vis.plt_normal_dist(dat_np)
