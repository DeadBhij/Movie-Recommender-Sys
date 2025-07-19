import streamlit as st
import pickle
import pandas as pd
import requests


SIMILARITY_PATH = "similarity.pkl"
CREDITS_PATH = "tmdb_5000_credits.csv"

similarity = pickle.load(open(SIMILARITY_PATH, "rb"))
credits = pd.read_csv(CREDITS_PATH)

st.title("Movie Recommender System")

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=82e06d2d7a7dc3f9cef0d30ff6a2b0c3')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

selected_movie_name = st.selectbox(
    "What kind of movie would you like to watch?",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])


st.markdown("""
    <style>
    .stApp {
        background-image: url("https://www.shutterstock.com/shutterstock/videos/1064609959/thumb/1.jpg?ip=x480");
        background-size: cover;
    }
    </style>
""", unsafe_allow_html=True)