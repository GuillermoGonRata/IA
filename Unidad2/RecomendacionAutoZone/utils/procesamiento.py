import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def cargar_datos(ruta): # Carga datos desde un archivo CSV y maneja errores si el archivo no existe
    return pd.read_csv(ruta)


def vectorizar_productos(df): # Convierte las descripciones de productos en una matriz TF-IDF *(Term Frequency-Inverse Document Frequency)*
     # Incluye nombre, categoría, marca y descripción (si existe)
    if 'descripcion' in df.columns:
        corpus = df['nombre'] + " " + df['categoria'] + " " + df['marca'] + " " + df['descripcion']
    else:
        corpus = df['nombre'] + " " + df['categoria'] + " " + df['marca']
    # Normaliza el texto
    corpus = corpus.str.lower().str.replace(r'[^a-z0-9\s]', '', regex=True) # Elimina caracteres especiales
    # Vectoriza usando TF-IDF
    vectorizador = TfidfVectorizer()
    matriz = vectorizador.fit_transform(corpus)
    return matriz, vectorizador
