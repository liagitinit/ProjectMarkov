from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from sklearn.preprocessing import normalize
from scipy.sparse import csr_matrix
from app.utils.model_prediction import get_movie_recommendation

# Cargar el modelo
knn_model = joblib.load('app/model/knn_model.joblib')

# Cargar los datos movies.csv y ratings.csv
movies = pd.read_csv('/src/data/movies.csv') # Usar ruta absoluta
ratings = pd.read_csv('/src/data/ratings.csv') # Usar ruta absoluta

# Preprocesamiento de datos para generar matriz de usuario-película
data = pd.pivot_table(ratings, values='rating', index='movieId', columns='userId', fill_value=0)

# Filtrar películas con menos de 10 votos y usuarios con menos de 50 votos
movie_counts = ratings['movieId'].value_counts()
user_counts = ratings['userId'].value_counts()
valid_movies = movie_counts[movie_counts >= 10].index
valid_users = user_counts[user_counts >= 50].index
filtered_ratings = ratings[(ratings['movieId'].isin(valid_movies)) & (ratings['userId'].isin(valid_users))]

# Nueva tabla de datos
data = pd.pivot_table(filtered_ratings, values='rating', index='movieId', columns='userId', fill_value=0)

# Crear matriz CSR para el modelo KNN
csr_data = csr_matrix(data.values)

# Normalizar los datos
csr_data_normalized = normalize(csr_data, norm='l2', axis=1)

# Inicializar la aplicación FastAPI
app = FastAPI()

# Definir el modelo de datos de entrada para la recomendación de películas
class MovieRequest(BaseModel):
    user_id: int

# Definir el endpoint de recomendación de películas
@app.post("/recommend/")
def recommend(request: MovieRequest):
    user_id = request.user_id

    recommended_movies = get_movie_recommendation(user_id, knn_model, csr_data_normalized, data, movies)

    if recommended_movies is not None:
        return recommended_movies.reset_index().to_dict(orient='records')
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Incluir el endpoint para probar si la API está funcionando
@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie Recommendation API"}
