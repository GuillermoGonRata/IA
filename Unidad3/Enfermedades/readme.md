# Sistema Experto para Diagnóstico Respiratorio

## Descripción General
El Sistema Experto para Diagnóstico Respiratorio es una aplicación web desarrollada en Python que utiliza técnicas de inteligencia artificial para ayudar en el diagnóstico de enfermedades respiratorias comunes. La aplicación guía al usuario a través de un cuestionario interactivo y proporciona diagnósticos basados en reglas médicas predefinidas.

## Estructura del Proyecto:
sistema-experto-respiratorio/
├─ app.py                    <- Aplicación principal con interfaz Streamlit.
├─ motor_inferencia.py       <- Motor de inferencia y lógica de diagnóstico.
├─ reglas_enfermedades.py    <- Base de conocimiento con reglas médicas.
└─ README.md                 <- Este archivo.

## Enfermedades
Enfermedad	    Síntomas Clave	                Contagiosidad	Duración
COVID-19	    Tos, Fiebre, Disnea	            ALTA	        7-14 días
Influenza	    Tos, Fiebre	                    ALTA	        5-7 días
Asma	        Disnea, Sibilancias	            NO_APLICA	    CRÓNICA
Neumonía	    Fiebre, Tos, Disnea	            MODERADA	    10-14 días
Resfriado       Común	Congestión nasal,       MODERADA	    3-7 días
                Dolor de garganta	
Bronquitis      Aguda	Tos, Expectoración	    BAJA	        7-10 días
Tuberculosis	Tos prolongada, Fiebre,         ALTA	        VARIOS_MESES
                Sudoración	

## Prerrequisitos:
    Python 3.8 o superior
    pip (gestor de paquetes de Python)

## Ejecucion:
Instalar dependencias:
    Primero instalar las dependencias con este comando:
        python -m pip install streamlit pandas

    Debes de ir al directorio donde se encuentra el archivo App.py para ejecutarlo
        cd c:\Users\Guill\Desktop\Enfermedades\IA\Unidad3\Enfermedades    
    
    Despues ejecutarlo con este comando.
        python -m streamlit run app.py

## Flujo de Diagnóstico

### Ingreso de Datos Demográficos
Primero el usuario debera ingresar sus datos Demograficos al sistema, este le pedira ingresar lo siguiente:
- Edad del paciente
- Hábito de tabaquismo

### Evaluación de Síntomas

 Despues debera contestar varias preguntas sobre los sintemas que tiene le usuario, las cuales englobaran lo siguiente:
- Síntomas principales (tos, fiebre, dificultad respiratoria)
- Síntomas adicionales (congestión nasal, dolor de garganta, etc.)
- Hallazgos físicos (crepitantes, ronquidos)
- Exámenes de laboratorio (PCR, radiografía)

### Proceso de Diagnóstico
El motor evalúa coincidencias con enfermedades conocidas
Calcula porcentajes de certeza basados en síntomas presentes
Prioriza resultados por probabilidad

### Resultados
Finalmente el programa arrojara como respuestas los siguientes puntos como un diagnostico final:
- Lista de posibles diagnósticos ordenados por certeza
- Explicación detallada del razonamiento
- Recomendaciones médicas
El programa dara un diagnostico certero cuando tenga un 90% de certeza en una enfermedad, si el programa no consigue ese 90%, tendra que precionar el boton de "Realizar diagnostico", para que le de un porcentaje de certeza y la posible enfermedad que tenga, junto con la explicacion detallada

## Base de Conocimiento
### Estructura de Reglas
Cada enfermedad está definida por el siguiente reglamento:
    "NOMBRE DE LA ENFERMEDAD": {
        "sintomas_obligatorios": [],    # Síntomas que deben estar presentes
        "sintomas_comunes": [],         # Síntomas que aumentan la certeza
        "examenes": [],                 # Pruebas de laboratorio relevantes
        "factores_riesgo": [],          # Grupos de edad de riesgo
        "tabaquismo": "SI/NO",          # Relación con tabaquismo
        "contagiosidad": "NIVEL",       # Grado de contagio
        "duracion": "RANGO"             # Duración típica o si es cronica
    }

### Agregar Nuevas Enfermedades
Para agregar una nueva enfermedad, edite el archivo reglas_enfermedades.py:
    "NUEVA_ENFERMEDAD": {
        "sintomas_obligatorios": ["SINTOMA1", "SINTOMA2"],
        "sintomas_comunes": ["SINTOMA3", "SINTOMA4"],
        "examenes": ["EXAMEN1"],
        "factores_riesgo": ["GRUPO_EDAD"],
        "tabaquismo": "NO",
        "contagiosidad": "MODERADA",
        "duracion": "7-10/cronica"
    }

### Algoritmo de Inferencia
Coincidencia Completa: Verifica si todos los síntomas obligatorios están presentes

Cálculo de Certeza:
- 90% base por síntomas obligatorios completos
- 30% adicional por síntomas comunes presentes
Priorización: Ordena resultados por porcentaje de certeza descendente

## Limitaciones Técnicas
- Base de conocimiento limitada a enfermedades predefinidas
- No considera historial médico completo
- No incluye imágenes médicas o resultados complejos de laboratorio
