import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
sns.set()# Helper functions
import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import time 

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="76f8001ab55843ac979a4728d3ed78c8",
                                                client_secret="8d93518878eb4da09dff1123fb4f73ac",
                                                redirect_uri="http://localhost:8888/callback",
                                                scope="user-top-read"))

def find_top_artists():
    '''
        Output: finds user's top artist for three time periods (short term, medium term, long term)
    '''
    artists = {}

    for sp_range in ['short_term', 'medium_term', 'long_term']:
        results = sp.current_user_top_artists(time_range=sp_range, limit=1)
        if results:
            artists[sp_range] = results['items'][0]['name']
        time.sleep(0.1)
    return artists


def get_artist_uri(name):
    '''
        Input: artist name
        Output: artist uri
    '''
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0 and items[0]["uri"]:
        return items[0]["uri"]
    else:
        return None


def find_artist_top_song(artist_uri):
    '''
        Input: artist uri
        Output: the artist's most popular song
    '''
    results = sp.artist_top_tracks(artist_uri, country="US")
    
    if results and results["tracks"] and results["tracks"][0] and results["tracks"][0]["name"] and results["tracks"][0]["id"]:
        return (results["tracks"][0]["name"], results["tracks"][0]["id"])

def find_song_danceability(song_id):
    '''
        Intput: a song id
        Output: the danceability score of the song
    '''
    results = sp.audio_features(song_id)
    if results and results[0]["danceability"]:
        return results[0]["danceability"]# Retrieve data
data = pd.read_csv("spotify.csv")
data.head()# Data exploration
data.info()
data.isnull().sum()
df = data.drop(columns=['id', 'name', 'artists', 'release_date', 'year'])
df.corr()# Data transformation
from sklearn.preprocessing import MinMaxScaler
datatypes = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
normarization = data.select_dtypes(include=datatypes)
for col in normarization.columns:
    MinMaxScaler(col)

from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=10)
features = kmeans.fit_predict(normarization)
data['features'] = features
MinMaxScaler(data['features'])# Spotify recommender
class Spotify_Recommendation():
    def __init__(self, dataset):
        self.dataset = dataset
    def recommend(self, songs, amount=1):
        distance = []
        song = self.dataset[(self.dataset.name.str.lower() == songs.lower())].head(1).values[0]
        rec = self.dataset[self.dataset.name.str.lower() != songs.lower()]
        for songs in tqdm(rec.values):
            d = 0
            for col in np.arange(len(rec.columns)):
                if not col in [1, 6, 12, 14, 18]:
                    d = d + np.absolute(float(song[col]) - float(songs[col]))
            distance.append(d)
        rec['distance'] = distance
        rec = rec.sort_values('distance')
        columns = ['artists', 'name']
        return rec[columns][:amount]

recommendations = Spotify_Recommendation(data)
recommendations.recommend("Lovers Rock", 10)