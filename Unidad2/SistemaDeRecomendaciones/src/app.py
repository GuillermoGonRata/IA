import os
import streamlit as st
import pandas as pd
from models.recommender import Recommender

# Carga los datos de películas y ratings desde archivos CSV.
movies_path = 'src/data/movies.csv'
ratings_path = 'src/data/ratings.csv'
users_path = 'src/data/users.csv'

movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)

# Intentar cargar users.csv, si no existe crear nombres por defecto
if os.path.exists(users_path):
    users = pd.read_csv(users_path)
else:
    unique_user_ids = sorted(ratings['userId'].unique())
    users = pd.DataFrame({'userId': unique_user_ids, 'username': [f'User {uid}' for uid in unique_user_ids]})

# Une los ratings con la información de las películas.
data = ratings.merge(movies, left_on='movieId', right_on='movieId')

# Inicializa el sistema de recomendación con los datos combinados.
recommender = Recommender(data)
recommender.fit()

# Título de la aplicación web.
st.title("Sistema de Recomendación de Películas")

# Permite al usuario seleccionar su nombre y ver también su id en el menú desplegable.
user_ids = sorted(data['userId'].unique())
labels = []
label_to_id = {}
for uid in user_ids:
    row = users[users['userId'] == uid]
    if not row.empty:
        uname = row['username'].iloc[0]
    else:
        uname = f'User {uid}'
    label = f"{uname} (id={uid})"
    labels.append(label)
    label_to_id[label] = int(uid)

selected_label = st.selectbox("Selecciona un usuario", labels)
user_id = label_to_id[selected_label]

# Permite al usuario elegir cuántas recomendaciones quiere ver (entre 1 y 20).
n = st.slider("¿Cuántas recomendaciones quieres ver?", 1, 20, 5)

# Cuando el usuario presiona el botón, se generan y muestran las recomendaciones.
if st.button("Mostrar recomendaciones"):
    recommendations = recommender.recommend(user_id, n)
    if recommendations:
        st.subheader(f"Recomendaciones para {selected_label}:")
        for idx, movie in enumerate(recommendations, 1):
            st.write(f"{idx}. {movie}")
    else:
        st.info("No hay recomendaciones disponibles para este usuario.")