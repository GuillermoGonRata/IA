import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def cargar_datos(ruta):
    return pd.read_csv(ruta)


def vectorizar_productos(df):
    # Incluye nombre, categoría, marca y descripción (si existe)
    if 'descripcion' in df.columns:
        corpus = df['nombre'] + " " + df['categoria'] + " " + df['marca'] + " " + df['descripcion']
    else:
        corpus = df['nombre'] + " " + df['categoria'] + " " + df['marca']
    # Normaliza el texto
    corpus = corpus.str.lower().str.replace(r'[^a-z0-9\s]', '', regex=True)
    vectorizador = TfidfVectorizer()
    matriz = vectorizador.fit_transform(corpus)
    return matriz, vectorizador
