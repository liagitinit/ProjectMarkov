from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Cargar el modelo
knn_model = joblib.load('app/model/knn_model.joblib')

# Inicializar la aplicación FastAPI
app = FastAPI()

# Definir el modelo de datos de entrada
class UserRequest(BaseModel):
    user_id: int

# Definir el endpoint de predicción
@app.post("/predict/")
def predict(request: UserRequest):
    user_id = request.user_id
    recommended_movies = predict_movies(user_id, knn_model, csr_data_normalized, data, movies)
    if recommended_movies is not None:
        return recommended_movies[['movieId', 'title']].to_dict(orient='records')
    else:
        return {"error": "User not found"}
