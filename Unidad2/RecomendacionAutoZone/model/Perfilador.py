import pandas as pd
from datetime import datetime


def validar_producto(producto_id, df_productos): # Verifica si el producto existe en el DataFrame
    return producto_id in df_productos['id_producto'].values

def productos_preferidos(id_usuario, df_historial, top_n=3): # Devuelve los productos más comprados por un usuario
    compras_usuario = df_historial[df_historial['id_usuario'] == id_usuario]
    conteo = compras_usuario['id_producto'].value_counts()
    return conteo.head(top_n).index.tolist() # Lista de IDs de productos preferidos


def registrar_compra(usuario_id, producto_id, ruta="data/historial.csv"): # Registra una compra en el historial
    nueva_fila = pd.DataFrame([{
        "id_usuario": usuario_id,
        "id_producto": producto_id,
        "tipo_interaccion": "compra",
        "fecha": datetime.today().strftime('%Y-%m-%d')# Formato de fecha AAAA-MM-DD
    }])
    try: # Intenta leer el archivo existente y agregar la nueva compra
        historial = pd.read_csv(ruta)
        historial = pd.concat([historial, nueva_fila], ignore_index=True)
    except FileNotFoundError: # Si no existe, crea uno nuevo
        historial = nueva_fila
    historial.to_csv(ruta, index=False)
