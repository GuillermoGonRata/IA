from sklearn.metrics.pairwise import cosine_similarity


def recomendar(producto_id, matriz, df, top_n=10):
    idx = df[df['id_producto'] == producto_id].index[0]
    similitudes = cosine_similarity(matriz[idx], matriz).flatten()
    indices = similitudes.argsort()[-top_n-1:-1][::-1]
    return df.iloc[indices]
