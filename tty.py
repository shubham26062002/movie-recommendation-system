from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
import pickle

df = pd.read_csv('main_data.csv')
df['movie_title'] = df['movie_title'].str.replace(r'[^\w\s]+', ' ').str.lower().str.strip()

title_map = dict(zip(df['movie_title'], df['movie_title']))

cv = CountVectorizer(stop_words='english')

vector = cv.fit_transform(df['comb'])

similarity = cosine_similarity(vector)
def get_recommendations(title, cosine_sim=similarity, title_map=title_map, keywords=None, num_recs=10):
    movie_title = title.lower().strip()
    
    matching_titles = []
    for t in title_map.keys():
        if fuzz.token_set_ratio(movie_title, t.lower()) >= 75:
            if t in title_map and not t.isdigit():
                matching_titles.append(t.lower())
    
    if not matching_titles:
        return []
    
  
    sim_scores = []
    for t in matching_titles:
        idx = df[df['movie_title'] == t].index[0]
        sim_scores.append((idx, cosine_sim[idx][idx]))
    
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:num_recs]
    movie_indices = [i[0] for i in sim_scores]
    movie_titles = [title_map[df['movie_title'].iloc[i]] for i in movie_indices]
    
    if keywords:
        filtered_movies = []
        for movie in movie_titles:
            genres = df[df['movie_title'] == movie]['genres'].values[0].split('|')
            for keyword in keywords:
                if keyword.lower() in movie.lower() or keyword.lower() in genres[0].lower():
                    filtered_movies.append(movie)
        return filtered_movies
    
    else:
        return movie_titles

recs = get_recommendations("liar liar", num_recs=10)
print(recs) 

objects_to_dump = {
    'cv': cv,
    'similarity': similarity,
    'title_map': title_map
}

# Open a file with the write binary mode
with open('recommender.pkl', 'wb') as f:
    # Dump the dictionary object into the file
    pickle.dump(objects_to_dump, f)
