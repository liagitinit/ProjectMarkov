import pandas as pd
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix

def predict_movies(user_id, model, csr_data_normalized, data, movies, n=5):
    try:
        user_idx = data.columns.get_loc(user_id)

        distances, indices = model.kneighbors(csr_data_normalized[user_idx].reshape(1, -1), n_neighbors=n+1)

        recommended_movie_ids = [data.index[idx] for idx in indices.flatten()[1:]]
        recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]

        return recommended_movies
    except KeyError:
        return None
