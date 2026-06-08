import streamlit as st
import requests
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def parse_features(text):
    try:
        data = ast.literal_eval(text)
    except Exception:
        return []
    if isinstance(data, list):
        return [item['name'].replace(' ', '') for item in data if 'name' in item]
    return []

def parse_cast(text):
    try:
        data = ast.literal_eval(text)
    except Exception:
        return []
    if isinstance(data, list):
        return [item['name'].replace(' ', '') for item in data[:5] if 'name' in item]
    return []

def parse_crew(text):
    try:
        data = ast.literal_eval(text)
    except Exception:
        return []
    crew = []
    if isinstance(data, list):
        for item in data:
            if item.get('job') == 'Director' and 'name' in item:
                crew.append(item['name'].replace(' ', ''))
    return crew

@st.cache_resource
def load_data():
    movies_df = pd.read_csv('dataset/tmdb_5000_movies.csv')
    credits_df = pd.read_csv('dataset/tmdb_5000_credits.csv')
    
    movies_df = movies_df[['id','title','overview','genres','keywords']]
    credits_df = credits_df[['movie_id','cast','crew']]
    movies_df = movies_df.merge(credits_df, left_on='id', right_on='movie_id')
    
    movies_df['genres'] = movies_df['genres'].apply(parse_features)
    movies_df['keywords'] = movies_df['keywords'].apply(parse_features)
    movies_df['cast'] = movies_df['cast'].apply(parse_cast)
    movies_df['crew'] = movies_df['crew'].apply(parse_crew)
    
    movies_df['overview'] = movies_df['overview'].fillna('').apply(lambda x: x.split())
    movies_df['tags'] = movies_df['overview'] + movies_df['genres'] + movies_df['keywords'] + movies_df['cast'] + movies_df['crew']
    movies_df['tags'] = movies_df['tags'].apply(lambda x: ' '.join(x).lower())
    
    new_df = movies_df[['movie_id','title','tags']]
    
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(new_df['tags'])
    similarity_matrix = cosine_similarity(vectors)
    
    return new_df[['movie_id','title']], similarity_matrix

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies, similarity = load_data()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie, movies, similarity)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])