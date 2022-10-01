import const as CONST

####################################################################################################################
# Get Data of the Currently Playing Song
def get_currently_playing_data(spotianalyze_object):
    spotify_object = spotianalyze_object.SPOTIFY_OBJECT

    playlist_uri = None

    raw_json = spotify_object.current_user_playing_track()

    name = raw_json[CONST.ITEM][CONST.NAME]
    artists = raw_json[CONST.ITEM][CONST.ARTISTS]
    duration = raw_json[CONST.ITEM][CONST.DURATION_MS]
    track_id = raw_json[CONST.ITEM][CONST.ID]

    context = raw_json[CONST.CONTEXT][CONST.TYPE]
    if context == "playlist":
        playlist_uri = raw_json[CONST.CONTEXT][CONST.URI]
    progress = raw_json[CONST.PROGRESS_MS]
    is_playing = raw_json[CONST.IS_PLAYING]

    track_features = spotify_object.audio_features(track_id)

    current_playing_data = {
        CONST.NAME: name,
        CONST.ARTISTS: artists,
        CONST.DURATION_MS: duration,
        CONST.ID: track_id,
        CONST.CONTEXT: context,
        CONST.PROGRESS_MS: progress,
        CONST.IS_PLAYING: is_playing,
        CONST.PLAYLIST_URI: playlist_uri,
        CONST.DANCEABILITY: track_features[0][CONST.DANCEABILITY],
        CONST.ENERGY: track_features[0][CONST.ENERGY],
        CONST.KEY: track_features[0][CONST.KEY],
        CONST.LOUDNESS: track_features[0][CONST.LOUDNESS],
        CONST.SPEECHINESS: track_features[0][CONST.SPEECHINESS],
        CONST.INSTRUMENTALNESS: track_features[0][CONST.INSTRUMENTALNESS],
        CONST.ACOUSTICNESS: track_features[0][CONST.ACOUSTICNESS],
        CONST.LIVENESS: track_features[0][CONST.LIVENESS],
        CONST.VALENCE: track_features[0][CONST.VALENCE],
        CONST.TEMPO: track_features[0][CONST.TEMPO],
    }

    return current_playing_data