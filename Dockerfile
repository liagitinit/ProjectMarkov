FROM python:3.8-slim

# Establece el directorio de trabajo en /src
WORKDIR /src

# Copia el archivo de requisitos y luego instala las dependencias
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente al contenedor
COPY src /src

# Copia los archivos CSV al contenedor
COPY src/data/movies.csv /src/data/movies.csv
COPY src/data/ratings.csv /src/data/ratings.csv

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
