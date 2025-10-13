# Detector de Spam

## Hecho por>
Gonzalez Cardenaz Guillermo #22170672 <br>
Urias Lugo Guillermo #22170838

## Archivos
### rules.py
Define un conjunto de reglas heurísticas para detectar patrones comunes en correos electrónicos considerados spam. Cada regla encapsula una condición y una acción, y puede evaluarse sobre un diccionario de datos de correo (email_data).

### SpamIndex.py
Implementa un sistema de detección de spam basado en reglas heurísticas. Evalúa correos electrónicos simulados (como los de spam.csv) analizando el remitente, el asunto, los enlaces y el contenido textual, asignando una puntuación acumulativa que permite clasificar el mensaje como spam o legítimo.

### TestRules.py
Este archivo implementa pruebas unitarias para funciones de detección de spam definidas en el módulo rules.py. Utiliza el framework estándar unittest para validar que las reglas se comporten correctamente ante distintos tipos de correos electrónicos simulados.
Define dos métodos de prueba que simulan correos con distintos contenidos y evalúan si la función de regla devuelve el resultado esperado.

### Spam.csv
Este archivo contiene una colección de mensajes SMS etiquetados como spam o legítimos (ham). Se utiliza como dataset de prueba y validación para sistemas de detección de spam basados en reglas o modelos de aprendizaje automático. Es especialmente útil para:
- Evaluar la precisión de reglas heurísticas.
- Entrenar clasificadores supervisados.
- Simular escenarios reales de detección.

#### Para mas detalles de los archivos comentamos el codigo fuente 


## Como ejecutar 
Se ejecuta en el archivo SpamIndex.py y al momento de ejecutar se mostrara un archivo y su estimacion de legitimidad
<img width="1181" height="134" alt="image" src="https://github.com/user-attachments/assets/e6af2710-5b5a-45da-b363-230dc2dcc2da" />

Si desea ver mas mensajes por ejecucion de codigo tiene que poner la cantidad que desea en:
<img width="1128" height="591" alt="image" src="https://github.com/user-attachments/assets/6209d5ff-caeb-4899-a225-df704f583ca9" />


