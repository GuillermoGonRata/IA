# Sistema Experto para Diagnóstico Respiratorio

## Descripción General

El Sistema Experto para Diagnóstico Respiratorio es una aplicación web desarrollada en Python que utiliza técnicas de inteligencia artificial para ayudar en el diagnóstico de enfermedades respiratorias comunes. La aplicación guía al usuario a través de un cuestionario interactivo y proporciona diagnósticos basados en reglas médicas predefinidas.

## Estructura del Proyecto:
sistema-experto-respiratorio/
├─ app.py                    <- Aplicación principal con interfaz Streamlit.
├─ motor_inferencia.py       <- Motor de inferencia y lógica de diagnóstico.
├─ reglas_enfermedades.py    <- Base de conocimiento con reglas médicas.
├─ intrucciones.txt          <- Instrucciones de como ejecutar el programa.
└─ README.md                 <- Este archivo.

## Enfermedades Soportadas
Enfermedad	    Síntomas Clave	            Contagiosidad	Duración
COVID-19	    Tos, Fiebre, Disnea	        ALTA	        7-14 días
Influenza	    Tos, Fiebre	                ALTA	        5-7 días
Asma	        Disnea, Sibilancias	        NO_APLICA	    CRÓNICA
Neumonía	    Fiebre, Tos, Disnea	        MODERADA	    10-14 días
Resfriado       Común	Congestión nasal,   MODERADA	    3-7 días
                Dolor de garganta	
Bronquitis      Aguda	Tos, Expectoración	BAJA	        7-10 días
Tuberculosis	Tos prolongada, Fiebre,     ALTA	        VARIOS_MESES
                Sudoración	