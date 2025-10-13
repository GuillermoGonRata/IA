# Detector de Spam

## Hecho por>
Gonzalez Cardenaz Guillermo #22170672
Urias Lugo Guillermo #22170838


## 1. Recogida de datos

Se utilizó el dataset público [`spam.csv`](../data/spam.csv), que contiene mensajes etiquetados como "spam" o "ham" (legítimos).  
**Características del dataset:**

- **Remitente:** No disponible en este dataset.
- **Asunto:** No disponible en este dataset.
- **Contenido:** Disponible en la columna `Message`.
- **Enlaces:** Se detectan buscando patrones de URLs en el contenido.
- **Archivos adjuntos:** No disponible en este dataset.

El dataset fue adaptado para el análisis y la detección de spam, mapeando las columnas a la estructura esperada por el sistema.

## 2. Creación de reglas

Se desarrollaron reglas basadas en patrones comunes de spam, implementadas en [`src/SpamIndex.py`](../src/SpamIndex.py) y [`src/rules.py`](../src/rules.py):

- **Palabras clave:** Si el contenido contiene palabras como "gratis", "urgente", "win", "prize", "cash", "claim", se suma puntuación de spam.
- **Enlaces sospechosos:** Si el mensaje contiene enlaces (http, www), se suma puntuación.
- **Remitente sospechoso:** (No aplicable en este dataset, pero la regla existe para datasets con remitente).
- **Exceso de signos de exclamación o frases típicas de spam:** Se suma puntuación si se detectan patrones como "!!!" o frases como "100% gratis".


## 3. Clases y su funcionamiento




## 4. Reflexión y análisis

**Eficacia de las reglas:**
Las reglas basadas en palabras clave y enlaces detectan la mayoría de los mensajes spam, pero pueden generar falsos positivos si un mensaje legítimo contiene palabras sospechosas.

**Resultados:**
El sistema detecta correctamente la mayoría de los mensajes spam del dataset spam.csv.
Se recomienda probar con otros datasets y ajustar las reglas según los resultados.

**Conclusión**
Este proyecto proporciona una base sólida para comprender y experimentar con mecanismos de detección de spam. La modularidad del sistema permite agregar nuevas reglas o integrar modelos de machine learning en el futuro.
