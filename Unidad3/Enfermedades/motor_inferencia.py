import streamlit as st
from reglas_enfermedades import ENFERMEDADES

class MotorInferencia:
    def __init__(self):
        self.sintomas_usuario = {}
        self.factores_riesgo = {}
        self.examenes_usuario = {}
        
    def calcular_coincidencia(self, enfermedad, reglas):
        """Calcula el porcentaje de coincidencia con una enfermedad"""
        puntos = 0
        total_puntos = 0
        explicacion = []
        
        # Verificar sintomas obligatorios
        for sintoma in reglas["sintomas_obligatorios"]:
            total_puntos += 2
            if self.sintomas_usuario.get(sintoma) == "SI":
                puntos += 2
                explicacion.append(f"COINCIDE: {sintoma} (obligatorio)")
            else:
                explicacion.append(f"NO COINCIDE: {sintoma} (obligatorio - falta)")
        
        # Verificar sintomas comunes
        for sintoma in reglas["sintomas_comunes"]:
            total_puntos += 1
            if self.sintomas_usuario.get(sintoma) == "SI":
                puntos += 1
                explicacion.append(f"COINCIDE: {sintoma}")
            else:
                explicacion.append(f"NO COINCIDE: {sintoma}")
        
        # Verificar examenes
        for examen in reglas["examenes"]:
            total_puntos += 1.5
            if self.examenes_usuario.get(examen) == "SI":
                puntos += 1.5
                explicacion.append(f"COINCIDE: {examen} (examen)")
            else:
                explicacion.append(f"NO COINCIDE: {examen} (examen)")
        
        # Verificar factores de riesgo
        total_puntos += 1
        if self.factores_riesgo["edad"] in reglas["factores_riesgo"]:
            puntos += 1
            explicacion.append(f"COINCIDE: Edad de riesgo")
        else:
            explicacion.append(f"NO COINCIDE: Edad de riesgo")
        
        total_puntos += 0.5
        if self.factores_riesgo["tabaquismo"] == reglas["tabaquismo"]:
            puntos += 0.5
            explicacion.append(f"COINCIDE: Tabaquismo")
        else:
            explicacion.append(f"NO COINCIDE: Tabaquismo")
        
        if total_puntos > 0:
            certeza = (puntos / total_puntos) * 100 * reglas["certeza_base"]
            return min(certeza, 100), explicacion
        return 0, explicacion
    
    def diagnosticar(self):
        """Realiza el diagnostico basado en las reglas"""
        resultados = []
        
        for enfermedad, reglas in ENFERMEDADES.items():
            certeza, explicacion = self.calcular_coincidencia(enfermedad, reglas)
            if certeza > 10:  # Solo considerar enfermedades con al menos 10% de certeza
                resultados.append({
                    "enfermedad": enfermedad,
                    "certeza": certeza,
                    "explicacion": explicacion,
                    "duracion": reglas["duracion"],
                    "contagiosidad": reglas["contagiosidad"]
                })
        
        # Ordenar por certeza descendente
        resultados.sort(key=lambda x: x["certeza"], reverse=True)
        return resultados
    
    def mostrar_resultados(self, resultados):
        """Muestra los resultados del diagnostico"""
        
        if not resultados:
            st.warning("No se encontraron enfermedades que coincidan con los sintomas ingresados.")
            return
        
        for i, resultado in enumerate(resultados[:1]):  # Top 5 resultados
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"### {i+1}. {resultado['enfermedad']}")
                    st.write(f"**Duracion tipica:** {resultado['duracion']}")
                    st.write(f"**Contagiosidad:** {resultado['contagiosidad']}")
                
                with col2:
                    st.write(f"### {resultado['certeza']:.1f}%")
                    st.progress(resultado['certeza'] / 100)
                
                with st.expander("Ver explicacion detallada"):
                    for linea in resultado['explicacion']:
                        st.write(linea)
                
                st.write("---")
        
        # Recomendacion final
        if resultados[0]["certeza"] > 70:
            st.success(f"Diagnostico mas probable: {resultados[0]['enfermedad']}")
            st.info("Recomendacion: Consulte con un especialista para confirmar el diagnostico y realizar pruebas adicionales.")
        else:
            st.warning("No se encontro un diagnostico claro. Consulte con un medico para una evaluacion detallada.")