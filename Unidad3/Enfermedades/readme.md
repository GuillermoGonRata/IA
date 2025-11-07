# Sistema Experto para Diagnóstico Respiratorio



## Descripción General
El Sistema Experto para Diagnóstico Respiratorio es una aplicación web desarrollada en Python que utiliza técnicas de inteligencia artificial para ayudar en el diagnóstico de enfermedades respiratorias comunes. La aplicación guía al usuario a través de un cuestionario interactivo y proporciona diagnósticos basados en reglas médicas predefinidas.

## Hecho por:
Gonzalez Cardenas Guillermo #22170672 <br>
Urias Lugo Guillermo #22170838 <br>

## Estructura del Proyecto:
sistema-experto-respiratorio/ <br>
├─ app.py                    <- Aplicación principal con interfaz Streamlit. <br>
├─ motor_inferencia.py       <- Motor de inferencia y lógica de diagnóstico. <br>
├─ reglas_enfermedades.py    <- Base de conocimiento con reglas médicas. <br>
└─ README.md                 <- Este archivo. <br>

## Clases
### Clase reglas_enfermedades.py:
Esta clase funge como base de conocimientos y contiene los hechos y reglas de las enfermedades que serán tomados por el motor de inferencia para llegar a un diagnostico certero.
<img width="921" height="727" alt="image" src="https://github.com/user-attachments/assets/abeaa050-0211-4819-8368-5a2243d860ae" />

#### Actualizacion de esta clase:
Le agregamos la recomendacion a cada enfermedad que teniamos para que salga una mas acertada de acuerdo a la enfermedad

<img width="1063" height="722" alt="image" src="https://github.com/user-attachments/assets/bc571e1e-2b72-4b7e-bbdf-3c455c64231d" />

---------------------------------------------------------------------------------------------------------------


### Clase motor_inferencia.py:
Dentro de esta clase tenemos el método “tiene_coincidencia_completa” la cual se encarga de verificar que haya una coincidencia exacta de los síntomas del usuario con alguna enfermedad y lo hace en 3 pasos. 
Primero compara los síntomas obligatorios si uno no coincide, retorna falso y descarta la enfermedad.
Segundo revisa los factores de riesgo y si no coincide, retorna falso y descarta la enfermedad.
Y por tercero y último revisa si el tabaquismo es importante para determinar si la enfermedad coincide con los síntomas.
<img width="921" height="418" alt="image" src="https://github.com/user-attachments/assets/c780d379-99dc-411f-88ca-150e335ef954" />

 -------------------------------------------------------------------------------------------------------------


Método calcular_conciencia:
Primero obtiene la lista de síntomas obligatorios y comunes para evaluarlos posteriormente con la respuesta del usuario y va contando los que están presentes de acuerdo con si la respuesta del usuario fue un SI. Primero cuenta los síntomas obligatorios ya que estos son los mas importantes para la detección de las enfermedades y si falta alguno la certeza se va a reducir enormemente (máximo 50 % siendo originalmente un máximo de 70%). Luego va a hacer lo mismo con los síntomas comunes, pero estos pueden aportar hasta un máximo de 30% de certeza adicional.
Al final se genera una explicación que esta constituida con los síntomas obligatorios y comunes para al final retornar la certeza total y la explicación.

<img width="921" height="660" alt="image" src="https://github.com/user-attachments/assets/7b84c09b-7a15-4cc3-a9e0-e27d0c484216" />

------------------------------------------------------------------------------------------------------------------



Método diagnosticar:
Este metodo llama a los dos metodos anteriores para realizar su diagnostico. Primero llama a tiene_coincidentia_completa ya que este compara que los sintomas coincidan en un 100% con la enfermedad para su
diagnostico y si al final de las preguntas ninguno coincide se llama a calcular_coincidencia para retornar la enfermedad de mayor certeza.
Al final retorna una lista de diccionarios donde cada uno contiene: enfermedad, certeza y explicacion. 

 <img width="921" height="824" alt="image" src="https://github.com/user-attachments/assets/b90dde67-5a25-47be-bc24-e3b927e8c363" />

------------------------------------------------------------------------------------------------------------------

### Clase app.py
Esta clase es en pocas palabras la interfaz y funciona con un metodo main que tiene los siguientes metodos:

Metodo determinar_grupo_edad:
Este metodo se encarga de guardar y clasificar la edad (en años) que ingresa el usuario. Esto es importante ya que hay enfermedades que son mas riesgosas en ciertos grupos de edad.

<img width="624" height="330" alt="image" src="https://github.com/user-attachments/assets/b047f28d-abb5-4e5f-841c-ec800a1cb83b" />

------------------------------------------------------------------------------------------------------------------

Metodo pregunta_disponible:
Este metodo se encarga de revisar si una pregunta debe de mostrarse basandose en las respuestas previas. (Quizas no se vea mucho en ejecución debido a que hay muchas similitudes en los sintomas de la base de conocimiento).

<img width="423" height="131" alt="image" src="https://github.com/user-attachments/assets/d6bef361-9394-4f82-a39b-2330aba88749" />


-------------------------------------------------------------------------------------------------------------------


Metodo siguiente_indice:
Este se encarga de determinar mediante indices cual es la siguiente pregunta que debe mostrar al usuario. Se utiliza al responder cada pregunta con si o no o al presionar continuar.


<img width="472" height="100" alt="image" src="https://github.com/user-attachments/assets/d3837671-d11d-4ab3-bc34-eca78f0465fb" />


--------------------------------------------------------------------------------------------------------------------

Metodo anterior_indice:
Este se encarga de determinar mediante indices cual fue la anterior pregunta por si el usuario quiere volver

<img width="495" height="101" alt="image" src="https://github.com/user-attachments/assets/e44ff120-f46b-4348-bfad-126dd5aef652" />

---------------------------------------------------------------------------------------------------------------------
Arreglo de preguntas: Luego tenemos un arreglo con las preguntas disponibles y sus categorias son:
* Datos demograficos (edad y tabaquismo).
* Sintomas principales.
* Sintomas adicionales.
* Hallazgos fisicos.
* Examenes de laboratorio.
<img width="1217" height="324" alt="image" src="https://github.com/user-attachments/assets/163123fb-5c2c-4e1e-a0ea-098f9e428865" />

---------------------------------------------------------------------------------------------------------------------
seccion de la interfaz que se encargan de mostrar la pregunta actual y otra que muestra el historial de respuestas.
<img width="550" height="283" alt="image" src="https://github.com/user-attachments/assets/1bc965e8-7bcd-42be-8a0b-10199bdba3bd" />

----------------------------------------------------------------------------------------------------------------------

Metodo verificar_diagnostico temprano:
Este metodo se encarga de verificar si ya puede emitir un diagnostico de acuerdo a la certeza en base a las respuestas del usuario (le colocamos un minimo de 90 pero puede ser cambiado), tambien necesito un minimo de respuestas al que de momento le colocamos 3 pero podemos modificarlo de igual manera si es muy precipitado. Este metodo lo que hace es llamar a diversos metodos como el diagnosticar que esta en la clase motor:inferencia para realizar esas comparaciones y asegurarse de que este por encima de la certeza que ajustemos como minima para llegar a una conclusion 

<img width="589" height="487" alt="image" src="https://github.com/user-attachments/assets/3c3b1d6c-4bf6-403f-9bfc-2473004a61bb" />

-----------------------------------------------------------------------------------------------------------------------

Esta seccion de codigo se encarga de manejar la pregunta actual y los botones de la interfaz. Se divide en la parte en la que seleccionas tu edad y la parte de preguntas de si o no.
Aqui cada que se ingresa una respusta se avanza automaticamente a la siguiente pregunta o se muestra el diagnostico si es que se determina que ya se puede llegar a uno, adicionalmente se van guardando las respuestas para que el usuario pueda verlas si gusta.


<img width="882" height="556" alt="image" src="https://github.com/user-attachments/assets/9430a1af-8d4d-4c29-b8c6-156eb7da5cb1" />

------------------------------------------------------------------------------------------------------------------------
Esta seccion de codigo se encarga de mostrar un mensaje de cierre y un resumen de las preguntas con las respuestas del usuario y presenta dos botones,
uno que realiza el diagnostico final y otro que permite cambiar las respuestas (Aunque este ultimo no se que tan practico sea ya que se supone que un usuario debe hablar con la verdad cuando habla de su salud pero ya es tarde y me da miedo de cambiar el codigo y que ya no arranque :p).


<img width="989" height="612" alt="image" src="https://github.com/user-attachments/assets/60882796-3b8f-402d-9df6-5a27202f49f3" />

-------------------------------------------------------------------------------------------------------------------------
Y esta seccion se encarga de mostrar el diagnostico al que llego y porque llego a este (Mostrando los sintomas) y muestra sugerencias y/o recomendaciones de acuerdo a la enfermedad

<img width="839" height="687" alt="image" src="https://github.com/user-attachments/assets/010b2637-0ce3-4c4a-a6b9-d1276a79b23a" />

<img width="1027" height="331" alt="image" src="https://github.com/user-attachments/assets/89c5b1a7-6396-4655-9bc3-2ab8bc948cf5" />


---------------------------------------------------------------------------------------------------------------------------


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

## Pruebas de ejecucion
Imagen de la interfaz al momento de ejecutar el programa

<img width="1031" height="498" alt="image" src="https://github.com/user-attachments/assets/5f56097c-72a3-419b-908f-5fd8f8518e9c" />

--------------------------------------------------------------------------------------------------------------------------

Imagen de la interfaz despues de responder cierta cantidad de preguntas

<img width="801" height="546" alt="image" src="https://github.com/user-attachments/assets/b993acdf-753f-4b35-add3-124aaff30a71" />

---------------------------------------------------------------------------------------------------------------------------

Imagen de diagnostico despues de que el sistema experto haya determinado que puede realizar uno en base a la certeza

<img width="831" height="887" alt="image" src="https://github.com/user-attachments/assets/37471f59-0860-45bd-bb93-afe70ea7aeee" />

<img width="795" height="709" alt="image" src="https://github.com/user-attachments/assets/083af904-d5d4-4125-977a-93b15203d776" />


Nota: dejamos que se mostraran las dos enfermedades mas posibles ya que consideramos que el sistema experto debe ser una herramienta de apoyo mas que una respuesta final. mas que nada para asi evitarnos problemas legales en caso de querer darle seguimiento a esta herramienta
----------------------------------------------------------------------------------------------------------------------------
Aqui se muestra la respuesta del sistema experto cuando el usuario no da informacion (Cuando el usuario da no a todo)

<img width="755" height="210" alt="image" src="https://github.com/user-attachments/assets/ed96a715-7778-4c32-973c-1263221efe8a" />

-----------------------------------------------------------------------------------------------------------------------------

Y cuando el usuario da informacion parcial, es decir, insuficiente el sistema muestra lo siguiente:
primero muestra las enfermedades que mas coinciden pero no las da como un diagnostico en si si no que no puede llegar a un diagnostico por que la informacion es insuficientes.

<img width="656" height="603" alt="image" src="https://github.com/user-attachments/assets/3a2ddfdb-6f46-40c4-ab17-251473af3be6" />

------------------------------------------------------------------------------------------------------------------------------

<img width="702" height="800" alt="image" src="https://github.com/user-attachments/assets/da15715f-1380-43b1-a467-ae08ab9aee50" />

 -----------------------------------------------------------------------------------------------------------------------------
 
<img width="755" height="210" alt="image" src="https://github.com/user-attachments/assets/00839839-7f9d-4b25-a1c0-fff189d6942f" />

------------------------------------------------------------------------------------------------------------------------------


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
        "recomendaciones": []           # Recomendaciones para el usuario
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
        "recomendaciones": [
            "Recomendacion 1",
            "Recomendacion 2",
            "Recomendacion 3",
        ] 
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
