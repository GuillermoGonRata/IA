import pandas as pd
from datetime import datetime


def validar_producto(producto_id, df_productos):
    return producto_id in df_productos['id_producto'].values


def registrar_compra(usuario_id, producto_id, ruta="data/historial.csv"):
    nueva_fila = pd.DataFrame([{
        "id_usuario": usuario_id,
        "id_producto": producto_id,
        "tipo_interaccion": "compra",
        "fecha": datetime.today().strftime('%Y-%m-%d')
    }])
    try:
        historial = pd.read_csv(ruta)
        historial = pd.concat([historial, nueva_fila], ignore_index=True)
    except FileNotFoundError:
        historial = nueva_fila
    historial.to_csv(ruta, index=False)
