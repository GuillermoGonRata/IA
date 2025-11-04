from Datos import enfermedades
#Encadenamiento hacia adelante
def motor_inferencia(datos):
    resultados = []
    for enfermedad, info in enfermedades.items():
        if info["regla"](datos):
            resultados.append((enfermedad, info["certeza"]))
    return resultados


#Encadenamiento hacia adelante
def verificar_hipotesis(enfermedad, datos):
    if enfermedad in enfermedades:
        regla = enfermedades[enfermedad]["regla"]
        return regla(datos)
    return False