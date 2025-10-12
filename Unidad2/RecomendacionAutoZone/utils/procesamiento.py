import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def cargar_datos(ruta):
    return pd.read_csv(ruta)


def vectorizar_productos(df):
    corpus = df['categoria'] + " " + df['marca']
    vectorizador = TfidfVectorizer()
    matriz = vectorizador.fit_transform(corpus)
    return matriz, vectorizador
