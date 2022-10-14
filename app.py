import streamlit as st
import pickle
import pandas as pd
import requests

st.set_page_config(page_title="Movie-Recommender",page_icon=":movie_camera:")

pkl=pickle.load(open('movies.pkl','rb'))
movies=pd.DataFrame(pkl)
similarity_matrix=pickle.load(open('similarity.pkl','rb'))

def get_poster(mid):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        mid)
    data = requests.get(url)
    data=data.json()
    img_path=data['poster_path']
    img_href="https://image.tmdb.org/t/p/w500/" + img_path
    return img_href

def fetch_recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity_matrix[movie_index]
    info_id_dist = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    mov_list=[]
    mov_post=[]
    for i in info_id_dist:
        movie_id = movies.iloc[i[0]].movie_id
        mov_list.append(movies.iloc[i[0]].title)
        # fetch poster from API TMDB
        mov_post.append(get_poster(movie_id))
    return mov_list,mov_post


st.title("Movie Recommender System")
option = st.selectbox(
    'Type or select a movie from the dropdown',
    movies['title'].values)

if st.button('Recommend'):
    names,posts=fetch_recommend(option)
    col = st.columns(5)
    with col[0]:
        st.text(names[0])
        st.image(posts[0])
    with col[1]:
        st.text(names[1])
        st.image(posts[1])

    with col[2]:
        st.text(names[2])
        st.image(posts[2])
    with col[3]:
        st.text(names[3])
        st.image(posts[3])
    with col[4]:
        st.text(names[4])
        st.image(posts[4])


