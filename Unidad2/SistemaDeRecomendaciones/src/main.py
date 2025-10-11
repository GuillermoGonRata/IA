import pandas as pd
from models.recommender import Recommender

def main():
    # Define las rutas de los archivos de datos de películas y ratings.
    movies_path = 'src/data/movies.csv'
    ratings_path = 'src/data/ratings.csv'

    # Carga los datasets de películas y ratings en DataFrames de pandas.
    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path)

    # Une los ratings con la información de las películas usando 'movieId' como clave.
    # Esto crea un DataFrame combinado con toda la información relevante.
    data = ratings.merge(movies, left_on='movieId', right_on='movieId')

    # Inicializa el sistema de recomendación con el DataFrame combinado.
    recommender = Recommender(data)
    recommender.fit()  # (No hace nada en este ejemplo, pero se deja para futuras mejoras)

    NUM_USERS = 10  # Número de usuarios para mostrar recomendaciones (puedes cambiarlo)
    user_ids = data['userId'].unique()[:NUM_USERS]  # Selecciona los primeros NUM_USERS únicos

    # Para cada usuario seleccionado, genera y muestra las recomendaciones.
    for user_id in user_ids:
        recommendations = recommender.recommend(user_id)

        print(f"\nRecomendaciones para user_id={user_id}:")
        if recommendations:
            for idx, movie in enumerate(recommendations, 1):
                print(f"{idx}. {movie}")
        else:
            print("No hay recomendaciones disponibles.")

if __name__ == "__main__":
    main()