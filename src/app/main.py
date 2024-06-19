from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd

from app.utils.model_prediction import get_movie_recommendation

# Cargar el modelo
knn_model = joblib.load('app/model/knn_model.joblib')

# Cargar los datos movies.csv y ratings.csv
movies = pd.read_csv('src/data/movies.csv')
ratings = pd.read_csv('src/data/ratings.csv')

# Preprocesamiento de datos (ejemplo: unir movies y ratings)
data_final = pd.merge(ratings, movies, on='movieId', how='left')

# Inicializar la aplicación FastAPI
app = FastAPI()

# Definir el modelo de datos de entrada para la recomendación de películas
class MovieRequest(BaseModel):
    movie_name: str

# Definir el endpoint de recomendación de películas
@app.post("/recommend/")
def recommend(request: MovieRequest):
    movie_name = request.movie_name
    
    # Llamada a la función get_movie_recommendation sin csr_data_normalized
    recommended_movies = get_movie_recommendation(movie_name, knn_model, data_final, movies)
    
    if recommended_movies is not None:
        return recommended_movies.reset_index().to_dict(orient='records')
    else:
        raise HTTPException(status_code=404, detail="Movie not found")
