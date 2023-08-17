import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_posters(movie_id):
    api_key = '7f32b1bf21a83fac53a98ec991f8a576'  # Replace with your actual API key
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US')
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None  # Return None instead of "Poster not available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Assuming 'movieId' is the column name for movie IDs
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_posters(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_names, recommended_posters = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(recommended_names[0])
        st.image(recommended_posters[0])

    with col2:
        st.markdown(recommended_names[1])
        st.image(recommended_posters[1])
    with col3:
        st.markdown(recommended_names[2])
        st.image(recommended_posters[2])
    with col4:
        st.markdown(recommended_names[3])
        st.image(recommended_posters[3])
    with col5:
        st.markdown(recommended_names[4])
        st.image(recommended_posters[4])


