import streamlit as st
from utils.procesamiento import cargar_datos, vectorizar_productos
from model.Recomendador import recomendar
from model.Perfilador import productos_preferidos, registrar_compra
import pandas as pd
from datetime import datetime


def ejecutar_app():
    st.title("🔧 Recomendador AutoZone")

    df_productos = cargar_datos("data/productos.csv")
    df_usuarios = cargar_datos("data/usuarios.csv")
    df_historial = cargar_datos("data/historial.csv")
    matriz, _ = vectorizar_productos(df_productos)

    usuario = st.selectbox("Selecciona tu usuario", df_usuarios['nombre'])
    usuario_id = df_usuarios[df_usuarios['nombre']
                             == usuario]['id_usuario'].values[0]

    st.subheader("🔍 Recomendaciones basadas en tu historial:")
    preferidos = productos_preferidos(usuario_id, df_historial)

    for pid in preferidos:
        recomendados = recomendar(pid, matriz, df_productos)
        for _, fila in recomendados.iterrows():
            st.write(
                f"- {fila['nombre']} ({fila['categoria']}, {fila['marca']}) - ${fila['precio']}")

    st.subheader("🛒 Buscar y comprar productos:")
    producto_seleccionado = st.selectbox(
        "Selecciona un producto para comprar", df_productos['nombre'])
    producto_id = df_productos[df_productos['nombre']
                               == producto_seleccionado]['id_producto'].values[0]

    if st.button("Confirmar compra"):
        nueva_fila = pd.DataFrame([{
            "id_usuario": usuario_id,
            "id_producto": producto_id,
            "tipo_interaccion": "compra",
            "fecha": datetime.today().strftime('%Y-%m-%d')
        }])
        df_historial = pd.concat([df_historial, nueva_fila], ignore_index=True)
        df_historial.to_csv("data/historial.csv", index=False)
        st.success("✅ Compra registrada exitosamente.")
