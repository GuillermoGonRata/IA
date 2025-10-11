import pandas as pd

class Recommender:
    """
    Clase para recomendar películas a usuarios basada en ratings promedio de otros usuarios.
    """

    def __init__(self, data):
        """
        Inicializa el recomendador con el DataFrame de datos combinados (ratings + movies).

        Args:
            data (pd.DataFrame): DataFrame que contiene información de ratings y películas.
        """
        self.data = data

    def fit(self):
        """
        Método de ajuste. No realiza ninguna acción en este ejemplo simple,
        pero se deja para compatibilidad con posibles mejoras futuras.
        """
        pass  # No es necesario entrenar nada para este ejemplo simple

    def recommend(self, user_id, n=5):
        """
        Recomienda películas a un usuario que aún no ha visto, basándose en el promedio de ratings de otros usuarios.

        Args:
            user_id (int): ID del usuario al que se le harán recomendaciones.
            n (int): Número de recomendaciones a devolver.

        Returns:
            list: Lista de títulos de películas recomendadas.
        """
        # Películas que el usuario ya ha visto
        seen_movies = set(self.data[self.data['userId'] == user_id]['movieId'])

        # Películas no vistas por el usuario
        unseen = self.data[~self.data['movieId'].isin(seen_movies)]

        # Calcula el promedio de rating y el número de ratings por película
        movie_scores = unseen.groupby(['movieId', 'title']).agg({'rating': 'mean', 'userId': 'count'}).reset_index()

        # Opcional: filtra películas con pocas calificaciones (al menos 5 ratings)
        movie_scores = movie_scores[movie_scores['userId'] >= 5]

        # Ordena por rating promedio descendente y toma las mejores n
        top_movies = movie_scores.sort_values('rating', ascending=False).head(n)

        # Devuelve los títulos recomendados
        return top_movies['title'].tolist()