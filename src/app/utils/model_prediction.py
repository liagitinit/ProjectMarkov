import pandas as pd

def get_movie_recommendation(user_id, model, csr_data_normalized, data, movies, n=5):
    try:
        # Obtener el índice del usuario en los datos
        user_idx = data.columns.get_loc(user_id)

        # Calcular vecinos más cercanos basado en las características del usuario
        distances, indices = model.kneighbors(csr_data_normalized[user_idx].reshape(1, -1), n_neighbors=n+1)

        # Obtener IDs de películas recomendadas excluyendo la película consultada
        recommended_movie_ids = [data.index[idx] for idx in indices.flatten()[1:]]

        # Filtrar y obtener información detallada de las películas recomendadas
        recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]

        return recommended_movies[['movieId', 'title']]

    except KeyError:
        return None
