from sklearn.metrics.pairwise import cosine_similarity


def recomendar(producto_id, matriz, df, top_n=10):# Recomienda productos similares basados en la similitud del coseno
    idx = df[df['id_producto'] == producto_id].index[0]# Encuentra el índice del producto
    similitudes = cosine_similarity(matriz[idx], matriz).flatten()
    indices = similitudes.argsort()[-top_n-1:-1][::-1]
    return df.iloc[indices] # Devuelve los productos recomendados
