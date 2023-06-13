from auth import authorize
import sys
import pandas as pd
from tqdm import tqdm
import time


sp = authorize()
genres = sp.recommendation_genre_seeds()
n_recs = 100

data_dict = {'id': [], 'genre': [], 'track_name': [], 'artist_name': [],
             'valence': [], 'energy': [], 'popularity': [], 'danceability': []}

for genre in tqdm(genres):
    recs = sp.recommendations(genres=[genre], limit=n_recs)
    recs = eval(recs.json().replace('null', '-999').replace('false', 'False').replace('true', 'True'))['tracks']

    for track in recs:
        data_dict['id'].append(track['id'])
        data_dict['genre'].append(genre)
        track_meta = sp.track(track["id"])
        data_dict['track_name'].append(track_meta.name)
        data_dict['artist_name'].append(track_meta.album.artists[0].name)
        
        track_features = sp.track_audio_features(track['id'])
        data_dict['valence'].append(track_features.valence)
        data_dict['energy'].append(track_features.energy)
        data_dict['danceability'].append(track_features.danceability)
        data_dict['popularity'].append(track['popularity'])

        time.sleep(0.2)


df = pd.DataFrame(data_dict)
df.drop_duplicates(subset = "id", keep = "first", inplace = True)
df.to_csv("valence_arousal_dataset.csv", index = False)