import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import urllib3
import pickle
from flask import Flask, request, jsonify
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import numpy as np
import pickle
from flask_cors import CORS

filename = 'C:/Users/shubh/Desktop/CodingWorkspace/movie-recommendation-system/nlp_model.pkl'
clf = pickle.load(open(filename, 'rb'))
vectorizer = pickle.load(open('C:/Users/shubh/Desktop/CodingWorkspace/movie-recommendation-system/recommender.pkl','rb'))

def create_similarity():
    data = pd.read_csv('main_data.csv')
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity


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

def get_suggestions():
    data = pd.read_csv('main_data.csv')
    return list(data['movie_title'].str.capitalize())

app = Flask(__name__)

CORS(app)

@app.route("/movies")
def movies():
    suggestions = get_suggestions()
    regex = r'\u00b7e'
    suggestions= [re.sub(regex, "", suggestions) for suggestions in suggestions]
    suggestions= [ suggestions.strip() for suggestions in suggestions]
    return suggestions

@app.route("/movies/recommendations", methods=['POST'])
def recommendations():
    data = request.json
    if 'movie' in data:
        movie = data['movie']
        recommendations = get_recommendations(movie, num_recs=10)
        return jsonify(recommendations)
    else:
        return jsonify({"message": "Missing field 'movie' in request body."}), 400

sauce = urllib3.request("GET",'https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
soup = bs.BeautifulSoup(sauce,'lxml')
soup_result = soup.find_all("div",{"class":"text show-more__control"})

reviews_list = [] # list of reviews
reviews_status = [] # list of comments (good or bad)
for reviews in soup_result:
    if reviews.string:
        reviews_list.append(reviews.string)
            # passing the review to our model
        movie_review_list = np.array([reviews.string])
        movie_vector = vectorizer.transform(movie_review_list)
        pred = clf.predict(movie_vector)
        reviews_status.append('Good' if pred else 'Bad')

    # combining reviews and comments into a dictionary
movie_reviews = {reviews_list[i]: reviews_status[i] for i in range(len(reviews_list))}     
print(movie_reviews)

if __name__ == '__main__':
    app.run(debug=True, port=8001)