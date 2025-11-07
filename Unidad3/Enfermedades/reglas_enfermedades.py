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
    },
    
    "INFLUENZA": {
        "sintomas_obligatorios": ["TOS", "FIEBRE"],
        "sintomas_comunes": ["DISNEA_LEVE", "FATIGA", "CONGESTION_NASAL", "DOLOR_GARGANTA", "CEFALEA", "MIALGIAS"],
        "examenes": ["PCR_POSITIVA"],
        "factores_riesgo": ["MAYOR_65"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "5-7",
    },
    "ASMA": {
        "sintomas_obligatorios": ["DISNEA", "SIBILANCIAS"],
        "sintomas_comunes": ["TOS", "OPRESION_PECHO", "FATIGA"],
        "examenes": ["ESPIROMETRIA_REDUCIDA"],
        "factores_riesgo": ["HISTORIAL_FAMILIAR_ASMA"],
        "tabaquismo": "NO",
        "contagiosidad": "NO_APLICA",
        "duracion": "CRONICA",
        },
    "NEUMONIA": {
        "sintomas_obligatorios": ["FIEBRE", "TOS", "DISNEA"],
        "sintomas_comunes": ["DOLOR_PECHO", "EXPECTORACION", "CEFALEA", "MIALGIAS"],
        "examenes": ["RADIOGRAFIA_ANORMAL", "ESPUTO_POSITIVO"],
        "factores_riesgo": ["MAYOR_65", "INMUNODEPRESION"],
        "tabaquismo": "NO",
        "contagiosidad": "MODERADA",
        "duracion": "10-14",
    },
    "RESFRIADO_COMUN": {
        "sintomas_obligatorios": ["CONGESTION_NASAL", "DOLOR_GARGANTA"],
        "sintomas_comunes": ["TOS_LEVE", "FIEBRE_BAJA", "ESTORNUDOS"],
        "examenes": [],
        "factores_riesgo": [],
        "tabaquismo": "NO",
        "contagiosidad": "MODERADA",
        "duracion": "3-7",
    },
    "BRONQUITIS_AGUDA": {
        "sintomas_obligatorios": ["TOS", "EXPECTORACION"],
        "sintomas_comunes": ["FIEBRE_BAJA", "DISNEA_LEVE", "DOLOR_PECHO"],
        "examenes": ["RADIOGRAFIA_NORMAL"],
        "factores_riesgo": ["TABAQUISMO"],
        "tabaquismo": "SI",
        "contagiosidad": "BAJA",
        "duracion": "7-10",
    },
    "TUBERCULOSIS": {
        "sintomas_obligatorios": ["TOS_PROLONGADA", "FIEBRE", "SUDORACION_NOCTURNA"],
        "sintomas_comunes": ["PERDIDA_PESO", "FATIGA", "DOLOR_PECHO"],
        "examenes": ["ESPUTO_POSITIVO", "RADIOGRAFIA_ANORMAL"],
        "factores_riesgo": ["INMUNODEPRESION", "CONTACTO_TBC"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "VARIOS_MESES",
        },
    "H1N1": {
        "sintomas_obligatorios": ["TOS", "FIEBRE"],
        "sintomas_comunes": ["DISNEA_LEVE", "FATIGA", "CONGESTION_NASAL", "DOLOR_GARGANTA", "CEFALEA", "MIALGIAS"],
        "examenes": ["PCR_POSITIVA"],
        "factores_riesgo": ["MAYOR_65", "EMBARAZO"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "5-7"
    }
    
   
}