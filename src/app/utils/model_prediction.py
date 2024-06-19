import pandas as pd
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix

def get_movie_recommendation(movie_name, model, data_final, movies, n=10):
    movie_list = movies[movies['title'].str.contains(movie_name, case=False, na=False)]
    
    if len(movie_list) > 0:
        movie_idx = movie_list.iloc[0]['movieId']
        movie_idx = data_final[data_final['movieId'] == movie_idx].index[0]

        distances, indices = model.kneighbors(data_final.iloc[movie_idx].values.reshape(1, -1), n_neighbors=n+1)

        rec_movie_indices = sorted(list(zip(indices.squeeze(), distances.squeeze())), key=lambda x: x[1])[1:]

        recommend = []
        recommend_distances = []

        for val in rec_movie_indices:
            movie_idx = data_final.iloc[val[0]]['movieId']
            idx = movies[movies['movieId'] == movie_idx].index
            recommend.append(movies.iloc[idx]['title'].values[0])
            recommend_distances.append(val[1])

        df = pd.DataFrame({'Title': recommend, 'Distance': recommend_distances})
        df.set_index('Distance', inplace=True)

        return df
    else:
        return None
