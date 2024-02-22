


class Song:
    def __init__(self, name: str, duration_ms: int, explicit: bool, uri: str, danceability: float, energy: float, key: int,
                 speechiness: float, acousticness: float, instrumentalness: float, valence: float, tempo: float,
                 artists: list):
        self.name = name
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.uri = uri
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.valence = valence
        self.tempo = tempo
        self.artists = artists
