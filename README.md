# Analysis of Spotify API Data with Hierarchical Clustering
This repository is an attempt to perform machine learning methods on data from the spotify API. There are two fundemental pieces to this repository:   
- A set of functions designed to analyze, clean, and store data pulled from the Spotify API utilizing the spotipy python module.
- A Hierarchical Clustering module I built to gain more experience with machine learning algorithms and to analyze the data I had retrieved from spotify. Theoretically, this algorithm should work for any dataset provided to it in the proper format.

Really, all of this was to practice retrieval/organization of data, and gain an understanding of machine learning fundementals, which in that regard, I've succeeded, however, hierarchical clustering for this dataset didn't work particurally well as a method of analysis. I will likely attempt others in the future, but for now this project is on hold. Regardless, here's an overview of how it all works.

## Spotianalyze
The `spotianalyze.py` module contains functions that access, clean and store data pulled from the spotify API. This module relies on setting up a `Spotify` object from the `Spotipy` library, which handles authentication and scoping for the spotify API. Documentation on that can be found [here](https://spotipy.readthedocs.io/en/2.22.1/).

#### Functions
---
`spotianalyze.create_library(spotify_object: Spotify)`: This takes a `Spotify` object as a parameter (from Spotipy). It creates two csv files: `library.csv` and `artists.csv`. `library.csv` contains song data from a user's song library (Liked Songs on spotify), which includes:
- duration (ms)
- explicit (boolean)
- name
- popularity
- uri
- artist uri (can be converted to list using ast.literal_eval)
- danceability
- energy
- key
- loudness
- speechiness
- acousticness
- instrumentalness
- liveness
- valence
- tempo  
  
`artist.csv` contains a table of every artist, and associated that is in the song library, including:  

- artists (name)
- genres
- popularity
- uri  
It is important to note that the file path for these is specified as `data/{filename}`, and does not create the folder on its own (as of right now).  
Details on what all of the features really mean can be found on the spotify api documentation [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)  
---
`spotianalyze.get_playlist(spotify_object: Spotify)` retrieves the collection of playlists that exist within a user's spotify account, both created and saved. A selection can be made from the terminal, and the function returns the uri and name of the playlist

## Agglomerative Cluster
 
