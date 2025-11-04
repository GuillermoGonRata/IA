import streamlit as st
import pandas as pd

# Cargar dataset
df = pd.read_csv("EnferRespCompleto.csv")

# Mostrar dataset
st.title("🧠 Sistema Experto: Diagnóstico de Enfermedades Respiratorias")
st.write("### Base de Conocimientos (Dataset)")
st.dataframe(df)

# Preparar reglas
enfermedades = df.to_dict(orient="records")

# Síntomas posibles
sintomas = [
    "TOS", "FIEBRE", "DISNEA", "SIBILANCIA", "DOLOR_PECHO", "FATIGA", 
    "CREPITANTES", "RONQUIDOS", "PCR_POSITIVA", "RADIOGRAFIA_ANORMAL", 
    "CONGESTION_NASAL", "DOLOR_GARGANTA", "EXPECTORACION", "CEFALEA", 
    "MIALGIAS"
]
factores_riesgo = ["MAYOR_60", "MAYOR_65", "MAYOR_40", "MAYOR_50", "MAYOR_55", "MENOR_2", "MENOR_5", "INMUNODEPRIMIDO", "NO_RIESGO"]
tabaquismo_opciones = ["SÍ", "NO"]

# Interfaz de usuario
st.sidebar.header("📋 Ingreso de Síntomas y Signos")

edad = st.sidebar.selectbox("Edad del paciente", factores_riesgo)
tabaquismo = st.sidebar.selectbox("Tabaquismo", tabaquismo_opciones)

st.sidebar.subheader("Síntomas")
sintomas_ingresados = {}
for sintoma in sintomas:
    sintomas_ingresados[sintoma] = st.sidebar.selectbox(sintoma, ["NO", "SÍ", "LEVE"], key=sintoma)

# Botón de diagnóstico
if st.sidebar.button("🔍 Realizar Diagnóstico"):

    # Motor de inferencia
    resultados = []

    for enf in enfermedades:
        puntos = 0
        total_campos = 0
        explicacion = []

        # Comparar cada campo
        for key, value in enf.items():
            if key == "ENFERMEDAD":
                continue
            if key in sintomas_ingresados:
                total_campos += 1
                if str(value).upper() == str(sintomas_ingresados[key]).upper():
                    puntos += 1
                    explicacion.append(f"{key} coincidió")
                elif str(sintomas_ingresados[key]).upper() == "LEVE" and str(value).upper() == "LEVE":
                    puntos += 0.5
                    explicacion.append(f"{key} coincidió (leve)")
            elif key == "TABAQUISMO":
                total_campos += 1
                if str(value).upper() == tabaquismo.upper():
                    puntos += 1
                    explicacion.append("Tabaquismo coincidió")
            elif key == "EDAD_RIESGO":
                total_campos += 1
                if str(value).upper() == edad.upper():
                    puntos += 1
                    explicacion.append("Edad de riesgo coincidió")

        if total_campos > 0:
            certeza = (puntos / total_campos) * 100
            resultados.append((enf["ENFERMEDAD"], certeza, explicacion))

    # Ordenar por certeza
    resultados.sort(key=lambda x: x[1], reverse=True)

    # Mostrar resultados
    st.write("## 📊 Resultados del Diagnóstico")
    for enf, cert, expl in resultados[:3]:  # Top 3
        st.write(f"### {enf} - {cert:.1f}% de certeza")
        with st.expander("Ver explicación"):
            for e in expl:
                st.write(f"- {e}")
        st.progress(int(cert))

    # Recomendación
    if resultados[0][1] > 70:
        st.success(f"🔔 Diagnóstico más probable: **{resultados[0][0]}**")
        st.info("💡 Recomendación: Consulte con un especialista para confirmar el diagnóstico y realizar pruebas adicionales.")
    else:
        st.warning("⚠️ No se encontró un diagnóstico claro. Consulte con un médico para una evaluación detallada.")