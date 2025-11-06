import streamlit as st
from motor_inferencia import MotorInferencia

def main():
    st.set_page_config(
        page_title="Sistema Experto Respiratorio", 
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # CSS personalizado para quitar el outline amarillo
    st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .stButton button {
        width: 100%;
        border: 1px solid #4a4a4a;
        background-color: #262730;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        margin: 0.25rem 0;
        outline: none !important;
        box-shadow: none !important;
    }
    .stButton button:focus {
        outline: none !important;
        box-shadow: none !important;
        border-color: #4a4a4a !important;
    }
    .stButton button:hover {
        background-color: #3a3a4a;
        border-color: #6a6a6a;
    }
    .stButton button:active {
        background-color: #4a4a5a;
    }
    .diagnostico-box {
        background-color: #1E1E1E;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF4B4B;
        margin: 1rem 0;
    }
    .pregunta-actual {
        background-color: #1E1E1E;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #4a4a4a;
        margin: 1rem 0;
    }
    /* Quitar outline de todos los elementos de streamlit */
    .stNumberInput input:focus, .stSelectbox select:focus {
        outline: none !important;
        box-shadow: none !important;
        border-color: #4a4a4a !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("Chat de Diagnostico Respiratorio")
    st.write("Sistema Experto para Enfermedades Respiratorias")
    st.write("---")
    
    # Inicializar session state
    if 'step' not in st.session_state:
        st.session_state.step = 0
    if 'respuestas' not in st.session_state:
        st.session_state.respuestas = {}
    if 'diagnostico_realizado' not in st.session_state:
        st.session_state.diagnostico_realizado = False
    
    # Determinar grupo de edad basado en la edad ingresada
    def determinar_grupo_edad(edad):
        if edad < 2:
            return "MENOR_2"
        elif edad < 5:
            return "MENOR_5"
        elif edad <= 20:
            return "MAYOR_20"
        elif edad <= 40:
            return "MAYOR_40"
        elif edad <= 50:
            return "MAYOR_50"
        elif edad <= 55:
            return "MAYOR_55"
        elif edad <= 60:
            return "MAYOR_60"
        elif edad <= 65:
            return "MAYOR_65"
        else:
            return "MAYOR_65"
    
    # Mostrar progreso
    total_pasos = 16
    if st.session_state.step < total_pasos:
        progreso = st.session_state.step / total_pasos
        st.progress(progreso)
        st.write(f"Progreso: {st.session_state.step}/{total_pasos}")
        st.write("---")
    
    # Preguntas en orden
    preguntas = [
        {
            "categoria": "Datos Demograficos",
            "pregunta": "Ingrese su edad en anos:",
            "tipo": "numero",
            "key": "edad"
        },
        {
            "categoria": "Datos Demograficos", 
            "pregunta": "Fuma actualmente?",
            "opciones": ["SI", "NO"],
            "key": "tabaquismo"
        },
        {
            "categoria": "Sintomas Principales",
            "pregunta": "Tiene tos?",
            "opciones": ["SI", "NO"],
            "key": "TOS"
        },
        {
            "categoria": "Sintomas Principales",
            "pregunta": "Tiene fiebre?",
            "opciones": ["SI", "NO"],
            "key": "FIEBRE"
        },
        {
            "categoria": "Sintomas Principales",
            "pregunta": "Tiene dificultad para respirar?",
            "opciones": ["SI", "NO"],
            "key": "DISNEA"
        },
        {
            "categoria": "Sintomas Principales", 
            "pregunta": "Tiene silbidos al respirar?",
            "opciones": ["SI", "NO"],
            "key": "SIBILANCIA"
        },
        {
            "categoria": "Sintomas Principales",
            "pregunta": "Tiene dolor en el pecho?",
            "opciones": ["SI", "NO"],
            "key": "DOLOR_PECHO"
        },
        {
            "categoria": "Sintomas Principales",
            "pregunta": "Se siente fatigado?",
            "opciones": ["SI", "NO"],
            "key": "FATIGA"
        },
        {
            "categoria": "Sintomas Adicionales",
            "pregunta": "Tiene congestion nasal?",
            "opciones": ["SI", "NO"],
            "key": "CONGESTION_NASAL"
        },
        {
            "categoria": "Sintomas Adicionales",
            "pregunta": "Tiene dolor de garganta?",
            "opciones": ["SI", "NO"],
            "key": "DOLOR_GARGANTA"
        },
        {
            "categoria": "Sintomas Adicionales",
            "pregunta": "Tiene expectoracion?",
            "opciones": ["SI", "NO"],
            "key": "EXPECTORACION"
        },
        {
            "categoria": "Sintomas Adicionales",
            "pregunta": "Tiene dolor de cabeza?",
            "opciones": ["SI", "NO"],
            "key": "CEFALEA"
        },
        {
            "categoria": "Sintomas Adicionales",
            "pregunta": "Tiene dolores musculares?",
            "opciones": ["SI", "NO"],
            "key": "MIALGIAS"
        },
        {
            "categoria": "Hallazgos Fisicos",
            "pregunta": "Se escuchan crepitantes en la auscultacion?",
            "opciones": ["SI", "NO"],
            "key": "CREPITANTES"
        },
        {
            "categoria": "Hallazgos Fisicos",
            "pregunta": "Se escuchan ronquidos respiratorios?",
            "opciones": ["SI", "NO"],
            "key": "RONQUIDOS"
        },
        {
            "categoria": "Examenes de Laboratorio", 
            "pregunta": "Tiene PCR positiva?",
            "opciones": ["SI", "NO"],
            "key": "PCR_POSITIVA"
        },
        {
            "categoria": "Examenes de Laboratorio",
            "pregunta": "Tiene radiografia de torax anormal?",
            "opciones": ["SI", "NO"],
            "key": "RADIOGRAFIA_ANORMAL"
        }
    ]
    
    # Mostrar preguntas anteriores respondidas
    if st.session_state.step > 0 and st.session_state.step < len(preguntas):
        with st.expander("Ver respuestas anteriores", expanded=False):
            for i in range(st.session_state.step):
                pregunta = preguntas[i]
                if "tipo" in pregunta and pregunta["tipo"] == "numero":
                    respuesta = st.session_state.respuestas.get(pregunta["key"], "No respondido")
                    st.write(f"{pregunta['pregunta']} -> {respuesta} anos")
                else:
                    respuesta = st.session_state.respuestas.get(pregunta["key"], "No respondido")
                    st.write(f"{pregunta['pregunta']} -> {respuesta}")
    
    # Mostrar pregunta actual
    if st.session_state.step < len(preguntas):
        pregunta_actual = preguntas[st.session_state.step]
        
        st.markdown(f'<div class="pregunta-actual">', unsafe_allow_html=True)
        st.write(f"### {pregunta_actual['categoria']}")
        st.write(f"**{pregunta_actual['pregunta']}**")
        
        # Para pregunta de edad (numero)
        if "tipo" in pregunta_actual and pregunta_actual["tipo"] == "numero":
            edad = st.number_input("Edad:", min_value=0, max_value=120, value=30, step=1, key="edad_input")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Continuar", use_container_width=True, key="btn_continuar"):
                    st.session_state.respuestas[pregunta_actual['key']] = edad
                    st.session_state.step += 1
                    st.rerun()
            with col2:
                if st.button("Atras", use_container_width=True, key="btn_atras_edad") and st.session_state.step > 0:
                    st.session_state.step -= 1
                    st.rerun()
        else:
            # Para preguntas SI/NO, usar botones
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button(f"SI", use_container_width=True, key=f"si_{pregunta_actual['key']}"):
                    st.session_state.respuestas[pregunta_actual['key']] = "SI"
                    st.session_state.step += 1
                    st.rerun()
            with col2:
                if st.button(f"NO", use_container_width=True, key=f"no_{pregunta_actual['key']}"):
                    st.session_state.respuestas[pregunta_actual['key']] = "NO"
                    st.session_state.step += 1
                    st.rerun()
            with col3:
                if st.button("Atras", use_container_width=True, key=f"atras_{pregunta_actual['key']}") and st.session_state.step > 0:
                    st.session_state.step -= 1
                    st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Mostrar boton de diagnostico cuando todas las preguntas esten respondidas
    elif st.session_state.step == len(preguntas) and not st.session_state.diagnostico_realizado:
        st.markdown('<div class="diagnostico-box">', unsafe_allow_html=True)
        st.success("Todas las preguntas han sido respondidas!")
        st.write("### Resumen de respuestas:")
        
        for pregunta in preguntas:
            if "tipo" in pregunta and pregunta["tipo"] == "numero":
                respuesta = st.session_state.respuestas.get(pregunta["key"], "No respondido")
                st.write(f"{pregunta['pregunta']} -> {respuesta} anos")
            else:
                respuesta = st.session_state.respuestas.get(pregunta["key"], "No respondido")
                st.write(f"{pregunta['pregunta']} -> {respuesta}")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Realizar Diagnostico", type="primary", use_container_width=True, key="btn_diagnostico"):
                with st.spinner("Analizando sintomas..."):
                    motor = MotorInferencia()
                    
                    # Convertir edad a grupo de riesgo
                    edad_numero = st.session_state.respuestas.get('edad', 30)
                    grupo_edad = determinar_grupo_edad(edad_numero)
                    
                    # Pasar respuestas al motor
                    motor.sintomas_usuario = {k: v for k, v in st.session_state.respuestas.items() if k not in ['edad', 'tabaquismo']}
                    motor.factores_riesgo = {
                        "edad": grupo_edad,
                        "tabaquismo": st.session_state.respuestas.get('tabaquismo', 'NO')
                    }
                    motor.examenes_usuario = {
                        "PCR_POSITIVA": st.session_state.respuestas.get('PCR_POSITIVA', 'NO'),
                        "RADIOGRAFIA_ANORMAL": st.session_state.respuestas.get('RADIOGRAFIA_ANORMAL', 'NO')
                    }
                    
                    resultados = motor.diagnosticar()
                    st.session_state.resultados = resultados
                    st.session_state.diagnostico_realizado = True
                    st.rerun()
        with col2:
            if st.button("Editar Respuestas", use_container_width=True, key="btn_editar"):
                st.session_state.step = 0
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Mostrar resultados del diagnostico
    if st.session_state.diagnostico_realizado and 'resultados' in st.session_state:
        st.write("---")
        st.write("## Resultados del Diagnostico")
        
        motor = MotorInferencia()
        motor.mostrar_resultados(st.session_state.resultados)
        
        # Boton para reiniciar
        st.write("---")
        if st.button("Realizar Nuevo Diagnostico", use_container_width=True, type="primary", key="btn_nuevo"):
            for key in ['step', 'respuestas', 'diagnostico_realizado', 'resultados']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()