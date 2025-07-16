import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# file_id = "1F6KYsDqg_7nXflDtjLkYJNV-6PamOhOU"
# url = f"https://drive.google.com/uc?id={file_id}"
# output = "similarity.pkl"
#
# # Only download if not already present
# if not os.path.exists(output):
#     gdown.download(url, output, quiet=False)

st.title("Movie Recommender System")

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=82e06d2d7a7dc3f9cef0d30ff6a2b0c3'.format(movie_id))
    data =  response.json()
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

SIMILARITY_PATH = "similarity.pkl"
SIMILARITY_URL = "https://drive.google.com/file/d/1gLMCPBiQ736EPOX0IQpTACc5G_SZJ_Sv/view?usp=sharing"

if not os.path.exists(SIMILARITY_PATH):
    gdown.download(SIMILARITY_URL, SIMILARITY_PATH, quiet=False)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(
    "What kind of movie would you like to watch?",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i in range(5):
        with columns[i]:
            st.markdown(
                f"<h4 style='text-align: center; font-size: 20px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{names[i]}</h4>",
                unsafe_allow_html=True
            )
            st.image(posters[i], use_container_width=True)

st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://www.shutterstock.com/shutterstock/videos/1064609959/thumb/1.jpg?ip=x480");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)
