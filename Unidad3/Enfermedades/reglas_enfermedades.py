# Base de conocimiento con reglas programadas para enfermedades respiratorias

ENFERMEDADES = {
    "COVID-19": {
        "sintomas_obligatorios": ["TOS", "FIEBRE", "DISNEA"],
        "sintomas_comunes": ["DOLOR_PECHO", "FATIGA", "CONGESTION_NASAL", "DOLOR_GARGANTA", "EXPECTORACION", "CEFALEA", "MIALGIAS"],
        "examenes": ["PCR_POSITIVA", "RADIOGRAFIA_ANORMAL"],
        "factores_riesgo": ["MAYOR_60"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "7-14",
        "certeza_base": 0.9
    },
    
    "INFLUENZA": {
        "sintomas_obligatorios": ["TOS", "FIEBRE"],
        "sintomas_comunes": ["DISNEA_LEVE", "FATIGA", "CONGESTION_NASAL", "DOLOR_GARGANTA", "CEFALEA", "MIALGIAS"],
        "examenes": ["PCR_POSITIVA"],
        "factores_riesgo": ["MAYOR_65"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "5-7",
        "certeza_base": 0.85
    },
    
    # ... (mantén el resto de las enfermedades igual, pero asegúrate de que todos los valores sean "SI"/"NO")
}