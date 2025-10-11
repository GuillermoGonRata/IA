import streamlit as st
import pandas as pd
from models.recommender import Recommender

# Carga los datos de películas y ratings desde archivos CSV.
movies_path = 'src/data/movies.csv'
ratings_path = 'src/data/ratings.csv'
movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)
# Une los ratings con la información de las películas.
data = ratings.merge(movies, left_on='movieId', right_on='movieId')

# Inicializa el sistema de recomendación con los datos combinados.
recommender = Recommender(data)
recommender.fit()

# Título de la aplicación web.
st.title("Sistema de Recomendación de Películas")

# Permite al usuario seleccionar su ID de usuario desde un menú desplegable.
user_ids = data['userId'].unique()
user_id = st.selectbox("Selecciona un usuario", user_ids)

# Permite al usuario elegir cuántas recomendaciones quiere ver (entre 1 y 20).
n = st.slider("¿Cuántas recomendaciones quieres ver?", 1, 20, 5)

# Cuando el usuario presiona el botón, se generan y muestran las recomendaciones.
if st.button("Mostrar recomendaciones"):
    recommendations = recommender.recommend(user_id, n)
    if recommendations:
        st.subheader(f"Recomendaciones para user_id={user_id}:")
        for idx, movie in enumerate(recommendations, 1):
            st.write(f"{idx}. {movie}")
    else:
        st.info("No hay recomendaciones disponibles para este usuario.")