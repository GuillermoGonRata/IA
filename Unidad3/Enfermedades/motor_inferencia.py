import streamlit as st
from reglas_enfermedades import ENFERMEDADES

class MotorInferencia:
    def __init__(self):
        self.sintomas_usuario = {}
        self.factores_riesgo = {}
        self.examenes_usuario = {}
        
    def tiene_coincidencia_completa(self, enfermedad, reglas):  #Este metodo se encarga de verificar si hay una coincidencia completa
        # Verificar sintomas obligatorios                       # con los sintomas obligatorios de una enfermedad
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

    def calcular_coincidencia(self, enfermedad, reglas): # Este metodo calcula la certeza de una enfermedad
        obligatorios = reglas.get("sintomas_obligatorios", []) #basado en los sintomas obligatorios y comunes
        comunes = reglas.get("sintomas_comunes", [])    #proporcionando una explicacion detallada
                                                        #de los sintomas encontrados.
        # Verificar síntomas obligatorios
        if not obligatorios:
            return 0.0, []
            
        obligatorios_presentes = sum(1 for s in obligatorios 
                                   if self.sintomas_usuario.get(s) == "SI")
        
        # Si no están todos los obligatorios, certeza baja
        if obligatorios_presentes < len(obligatorios):
            certeza = (obligatorios_presentes / len(obligatorios)) * 50  # max 50%
            return certeza, [f"{obligatorios_presentes}/{len(obligatorios)} síntomas obligatorios"]
        
        # Verificar síntomas comunes
        comunes_presentes = sum(1 for s in comunes 
                              if self.sintomas_usuario.get(s) == "SI")
        
        # Calcular certeza total
        certeza_obligatorios = 70  # Base por tener todos los obligatorios
        certeza_comunes = 30 * (comunes_presentes / len(comunes)) if comunes else 0
        certeza_total = certeza_obligatorios + certeza_comunes
        
        explicacion = [
            f"Síntomas obligatorios: {obligatorios_presentes}/{len(obligatorios)}",
            f"Síntomas comunes: {comunes_presentes}/{len(comunes)}"
        ]
        
        return certeza_total, explicacion
    
    def diagnosticar(self):                                                         #Este metodo realiza el diagnostico
        # Primero buscar coincidencias completas                                    #llamando a los metodos anteriores
        for enfermedad, reglas in ENFERMEDADES.items():                             #y devolviendo los resultados
            if self.tiene_coincidencia_completa(enfermedad, reglas):                # con toda la informacion relevante
                return [{
                    "enfermedad": enfermedad,
                    "certeza": 100,
                    "explicacion": ["Coincidencia completa con síntomas obligatorios"],
                    "duracion": reglas["duracion"],
                    "contagiosidad": reglas["contagiosidad"],
                    "recomendaciones": reglas.get("recomendaciones", []),
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
                    "recomendaciones": reglas.get("recomendaciones", []),
                    "es_coincidencia_completa": False
                })
        
        resultados.sort(key=lambda x: x["certeza"], reverse=True)
        return resultados
    
    