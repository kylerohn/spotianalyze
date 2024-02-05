import spotianalyze
from IPython.display import display
from const import CONST as C


sp = spotianalyze.Spotianalyze('kyler4646', '46c3926db9ca4105b12141a1c9b20e0e',
                            'e09da8c8808d4ebeadddd2f1cdb50720', 'http://localhost/')

big_data = sp.liked_songs_parser()

for artists in big_data[C.ARTISTS]:
    for artist_genres in artists[C.GENRES]:
        print(artist_genres)
