import streamlit as st
from reglas_enfermedades import ENFERMEDADES

class MotorInferencia:
    def __init__(self):
        self.sintomas_usuario = {}
        self.factores_riesgo = {}
        self.examenes_usuario = {}
        
    def tiene_coincidencia_completa(self, enfermedad, reglas):
        """
        Verifica si hay una coincidencia completa con los síntomas obligatorios.
        """
        # Verificar sintomas obligatorios
        for sintoma in reglas["sintomas_obligatorios"]:
            if self.sintomas_usuario.get(sintoma) != "SI":
                return False
                
        # Verificar factores de riesgo críticos si existen
        if reglas["factores_riesgo"]:
            if self.factores_riesgo["edad"] not in reglas["factores_riesgo"]:
                return False
            
        # Verificar tabaquismo si es relevante
        if reglas["tabaquismo"] != "NO":  # Si el tabaquismo es importante para esta enfermedad
            if self.factores_riesgo["tabaquismo"] != reglas["tabaquismo"]:
                return False
                
        return True

    def calcular_coincidencia(self, enfermedad, reglas):
        """Calcula una certeza simple (%) basada en proporción de síntomas obligatorios presentes."""
        obligatorios = reglas.get("sintomas_obligatorios", [])
        if not obligatorios:
            return 0.0, []
        presentes = sum(1 for s in obligatorios if self.sintomas_usuario.get(s) == "SI")
        certeza = (presentes / len(obligatorios)) * 100
        explicacion = [f"{presentes}/{len(obligatorios)} síntomas obligatorios presentes"]
        return certeza, explicacion
    
    def diagnosticar(self):
        """Realiza el diagnostico basado en las reglas"""
        # Primero buscar coincidencias completas
        for enfermedad, reglas in ENFERMEDADES.items():
            if self.tiene_coincidencia_completa(enfermedad, reglas):
                return [{
                    "enfermedad": enfermedad,
                    "certeza": 100,
                    "explicacion": ["Coincidencia completa con síntomas obligatorios"],
                    "duracion": reglas["duracion"],
                    "contagiosidad": reglas["contagiosidad"],
                    "es_coincidencia_completa": True
                }]
        
        # Si no hay coincidencia completa, continuar con el diagnóstico normal
        resultados = []
        for enfermedad, reglas in ENFERMEDADES.items():
            certeza, explicacion = self.calcular_coincidencia(enfermedad, reglas)
            if certeza > 10:  # Solo considerar enfermedades con al menos 10% de certeza
                resultados.append({
                    "enfermedad": enfermedad,
                    "certeza": certeza,
                    "explicacion": explicacion,
                    "duracion": reglas["duracion"],
                    "contagiosidad": reglas["contagiosidad"],
                    "es_coincidencia_completa": False
                })
        
        resultados.sort(key=lambda x: x["certeza"], reverse=True)
        return resultados
    
    