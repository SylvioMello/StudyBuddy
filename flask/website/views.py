from flask import Blueprint, render_template, request, flash
import pandas as pd
from .music.auth import authorize
from .music.model import recommend

# definimos os 'caminhos'
views = Blueprint('views', __name__)

# página inicial
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        track_id = request.form.get('track_id')
        variables_to_dist = list(request.form)
        variables_to_dist.remove('track_id')

    sp = authorize()
    
    try: 
        sp.track(track_id)
    except:
        return render_template('base.html')
    

    
    link = f"https://open.spotify.com/embed/track/{track_id}?utm_source=generator"

    data = pd.read_csv('https://raw.githubusercontent.com/SylvioMello/MusicMentor/main/flask/website/music/spotify_data/data.csv')
    recommendations = recommend(track_id, data, sp, variables_to_dist = variables_to_dist)['id'].values.tolist()
    rec_links = []

    for rec_id in recommendations:
        rec_link = f"https://open.spotify.com/embed/track/{rec_id}?utm_source=generator"
        rec_links.append(rec_link)
    

    return render_template('base.html', your_song=link, recommendations_links=rec_links)