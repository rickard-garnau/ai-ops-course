import pandas as pd
import requests
import streamlit as st


def layout():
    st.title(" Chatbot")

    movie_string = st.text_input("Give me a statement and it will give back a movie")

    movie = requests.post(
        "http://127.0.0.1:8000/movie", json={"query": movie_string}
    ).json()

    st.write(movie)

    genre = st.selectbox(
        "Choose genre", options=["action", "comedy", "thriller", "horror"]
    )
    movies = requests.get(f"http://127.0.0.1:8000/movies?genre={genre}").json()
    st.dataframe(pd.DataFrame(movies))


def init_session_states():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        return []


if __name__ == "__main__":
    layout()
