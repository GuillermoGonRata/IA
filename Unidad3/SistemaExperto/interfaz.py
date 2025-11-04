import streamlit as st
from inferencia import motor_inferencia
from Datos import casos_prueba

st.title("Sistema Experto Evidence-03 🧠")

# Datos demográficos
edad = st.number_input("Edad del paciente", min_value=0)
sexo = st.selectbox("Sexo", ["Masculino", "Femenino", "Otro"])

# Síntomas
tos = st.selectbox("Tipo de tos", ["Ninguna", "Seca", "Productiva"])
duracion_tos = st.selectbox("Duración de la tos", ["<3 días", "3-7 días", ">7 días"])
disnea = st.checkbox("¿Tiene dificultad para respirar?")
sibilancias = st.checkbox("¿Presenta sibilancias?")
dolor_pecho = st.checkbox("¿Dolor en el pecho?")
fiebre = st.checkbox("¿Fiebre?")
fatiga = st.checkbox("¿Fatiga?")

# Factores de riesgo
tabaquismo = st.checkbox("Antecedentes de tabaquismo")
contaminantes = st.checkbox("Exposición a contaminantes")
alergias = st.checkbox("Antecedentes alérgicos o familiares")

# Hallazgos físicos/laboratorio
crepitantes = st.checkbox("Crepitantes en auscultación")
saturacion = st.slider("Saturación de oxígeno (%)", 70, 100)
rx_consolidacion = st.selectbox("Rx torácica: ¿Consolidación pulmonar?", ["Sí", "No"])
pcr = st.selectbox("PCR elevada", ["Sí", "No", "No disponible"])

datos_paciente = {
    "edad": edad,
    "sexo": sexo,
    "tos": tos,
    "duracion_tos": duracion_tos,
    "disnea": disnea,
    "sibilancias": sibilancias,
    "dolor_pecho": dolor_pecho,
    "fiebre": fiebre,
    "fatiga": fatiga,
    "tabaquismo": tabaquismo,
    "contaminantes": contaminantes,
    "alergias": alergias,
    "crepitantes": crepitantes,
    "saturacion": saturacion,
    "rx_consolidacion": rx_consolidacion,
    "pcr": pcr
}

def evaluar_sistema(casos):
    aciertos = 0
    for caso in casos:
        resultado = motor_inferencia(caso["datos"])
        diagnosticos = [r[0] for r in resultado]
        if caso["esperado"] in diagnosticos:
            aciertos += 1
    precision = aciertos / len(casos)
    return precision


if st.button("Diagnosticar"):
    resultado = motor_inferencia(datos_paciente)
    if resultado:
        for diag, certeza in resultado:
            st.success(f"Diagnóstico presuntivo: {diag} (Certeza: {certeza * 100:.1f}%)")
    else:
        st.warning("No se encontró un diagnóstico presuntivo con los datos ingresados.")


if st.button("Evaluar sistema con casos de prueba"):
    precision = evaluar_sistema(casos_prueba)
    st.info(f"Precisión del sistema en pruebas: {precision * 100:.1f}%")





