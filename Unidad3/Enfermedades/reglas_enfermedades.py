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
        "recomendaciones": [
            "AISLAMIENTO: Mantenga aislamiento estricto por 10-14 dias",
            "CONSULTA: Acuda inmediatamente a un centro medico para prueba PCR",
            "TRATAMIENTO: Puede requerir antivirales como Remdesivir",
            "MONITOREO: Controle su saturacion de oxigeno regularmente",
            "HIDRATACION: Beba abundantes liquidos y descanse",
            "URGENCIA: Si tiene dificultad respiratoria severa, acuda a emergencias"
        ]
    },
    
    "INFLUENZA": {
        "sintomas_obligatorios": ["TOS", "FIEBRE"],
        "sintomas_comunes": ["DISNEA", "FATIGA", "CONGESTION_NASAL", "DOLOR_GARGANTA", "CEFALEA", "MIALGIAS"],
        "examenes": ["PCR_POSITIVA"],
        "factores_riesgo": ["MAYOR_65"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "5-7",
        "recomendaciones": [
            "REPOSO: Guarde reposo absoluto por 5-7 dias",
            "MEDICACION: Tome Oseltamivir dentro de las primeras 48 horas",
            "HIDRATACION: Beba liquidos en abundancia",
            "ANTITERMICOS: Use paracetamol para controlar la fiebre",
            "AISLAMIENTO: Evite contacto con otras personas para prevenir contagio",
            "SEGUIMIENTO: Consulte si la fiebre persiste mas de 5 dias"
        ]
    },
    
    "ASMA": {
        "sintomas_obligatorios": ["DISNEA", "SIBILANCIA"],
        "sintomas_comunes": ["TOS", "DOLOR_PECHO", "FATIGA"],
        "examenes": ["ESPIROMETRIA_REDUCIDA"],
        "factores_riesgo": ["HISTORIAL_FAMILIAR_ASMA"],
        "tabaquismo": "NO",
        "contagiosidad": "NO_APLICA",
        "duracion": "CRONICA",
        "recomendaciones": [
            "INHALADORES: Use broncodilatadores de accion rapida durante la crisis",
            "CONSULTA: Acuda a neumologo para tratamiento de control",
            "EVITE DESENCADENANTES: Polvo, polen, humo y aire frio",
            "PLAN DE ACCION: Tenga un plan escrito para manejar las crisis",
            "MEDICACION: Puede requerir corticoides inhalados",
            "URGENCIA: Si el inhalador no alivia en 15 minutos, acuda a emergencias"
        ]
    },
    
    "NEUMONIA": {
        "sintomas_obligatorios": ["FIEBRE", "TOS", "DISNEA"],
        "sintomas_comunes": ["DOLOR_PECHO", "EXPECTORACION", "CEFALEA", "MIALGIAS"],
        "examenes": ["RADIOGRAFIA_ANORMAL", "ESPUTO_POSITIVO"],
        "factores_riesgo": ["MAYOR_65", "INMUNODEPRESION"],
        "tabaquismo": "NO",
        "contagiosidad": "MODERADA",
        "duracion": "10-14",
        "recomendaciones": [
            "ANTIBIOTICOS: Inicie tratamiento antibiotico inmediatamente",
            "HOSPITALIZACION: Puede requerir hospitalizacion segun severidad",
            "HIDRATACION: Beba abundantes liquidos",
            "OXIGENO: Puede necesitar oxigenoterapia",
            "REPOSO: Guarde reposo absoluto",
            "SEGUIMIENTO: Control radiografico despues del tratamiento"
        ]
    },
    
    "RESFRIADO_COMUN": {
        "sintomas_obligatorios": ["CONGESTION_NASAL", "DOLOR_GARGANTA"],
        "sintomas_comunes": ["TOS", "FIEBRE", "CEFALEA", "MIALGIAS"],
        "examenes": [],
        "factores_riesgo": [],
        "tabaquismo": "NO",
        "contagiosidad": "MODERADA",
        "duracion": "3-7",
        "recomendaciones": [
            "HIDRATACION: Beba liquidos calientes como te con miel",
            "DESCANSO: Descanse lo suficiente",
            "ANALGESICOS: Use paracetamol para malestar general",
            "HIGIENE: Lave sus manos frecuentemente para evitar contagiar",
            "VAPOR: Inhalaciones de vapor pueden aliviar la congestion",
            "CONSULTA: Si los sintomas empeoran o persisten mas de 7 dias"
        ]
    },
    
    "BRONQUITIS_AGUDA": {
        "sintomas_obligatorios": ["TOS", "EXPECTORACION"],
        "sintomas_comunes": ["FIEBRE", "DISNEA", "DOLOR_PECHO"],
        "examenes": ["RADIOGRAFIA_NORMAL"],
        "factores_riesgo": ["TABAQUISMO"],
        "tabaquismo": "SI",
        "contagiosidad": "BAJA",
        "duracion": "7-10",
        "recomendaciones": [
            "DEJE DE FUMAR: Suspenda el tabaquismo inmediatamente",
            "HIDRATACION: Beba abundantes liquidos para fluidificar secreciones",
            "EXPECTORANTES: Puede usar mucoliticos para facilitar la expectoracion",
            "HUMEDAD: Use humidificador en su habitacion",
            "REPOSO: Evite actividades extenuantes",
            "CONSULTA: Si la tos persiste mas de 3 semanas"
        ]
    },
    
    "TUBERCULOSIS": {
        "sintomas_obligatorios": ["TOS", "FIEBRE", "EXPECTORACION"],
        "sintomas_comunes": ["DOLOR_PECHO", "FATIGA", "PERDIDA_PESO"],
        "examenes": ["ESPUTO_POSITIVO", "RADIOGRAFIA_ANORMAL"],
        "factores_riesgo": ["INMUNODEPRESION", "CONTACTO_TBC"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "VARIOS_MESES",
        "recomendaciones": [
            "TRATAMIENTO: Inicie tratamiento con multiples antibioticos inmediatamente",
            "AISLAMIENTO: Mantenga aislamiento respiratorio hasta negativizacion",
            "NOTIFICACION: Es una enfermedad de notificacion obligatoria",
            "CONTACTOS: Todos los contactos cercanos deben ser evaluados",
            "CUMPLIMIENTO: Complete todo el tratamiento (6-9 meses)",
            "SEGUIMIENTO: Controles frecuentes durante todo el tratamiento"
        ]
    },
    
    "H1N1": {
        "sintomas_obligatorios": ["TOS", "FIEBRE"],
        "sintomas_comunes": ["DISNEA", "FATIGA", "CONGESTION_NASAL", "DOLOR_GARGANTA", "CEFALEA", "MIALGIAS"],
        "examenes": ["PCR_POSITIVA"],
        "factores_riesgo": ["MAYOR_65", "EMBARAZO"],
        "tabaquismo": "NO",
        "contagiosidad": "ALTA",
        "duracion": "5-7",
        "recomendaciones": [
            "ANTIVIRALES: Inicie Oseltamivir dentro de las primeras 48 horas",
            "AISLAMIENTO: Mantengase en casa por 7 dias o hasta 24 horas sin fiebre",
            "HIDRATACION: Beba abundantes liquidos",
            "REPOSO: Descanse completamente",
            "GRUPOS RIESGO: Embarazadas y adultos mayores requieren atencion inmediata",
            "VACUNACION: Considere vacunacion anual contra influenza"
        ]
    }
}