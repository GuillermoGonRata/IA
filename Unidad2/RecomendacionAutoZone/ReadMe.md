# Sistema de Recomendacion de productos Autozone

## Hecho por:
Gonzalez cardenas Guillermo #22170672 <br>
Urias Lugo Guillermo #22170838

## Archivos
### interfaz.py
Este archivo define la interfaz principal de usuario para el sistema de recomendación de productos de AutoZone, construido con la lógica de la aplicacion Streamlit. Permite seleccionar usuarios, generar recomendaciones personalizadas basadas en historial de compras, y registrar nuevas compras en tiempo real (para que se actualicen las recomendaciones despues de de realizar una compra hay que reiniciar la pagina del navegador).

### Perfilador.py
Este módulo forma parte del sistema de recomendación de AutoZone. Su propósito es gestionar el perfil de usuario, identificando sus productos preferidos y registrando sus compras en el historial. 

### Recomendador.py
Este módulo implementa la lógica de recomendación de productos para AutoZone, utilizando similitud del coseno sobre vectores TF-IDF. Su objetivo es sugerir productos similares al que el usuario ha comprado o seleccionado, basándose en características vectorizadas.

### Procesamiento.py
Este módulo contiene funciones esenciales para la preparación de datos en el sistema de recomendación AutoZone. Se encarga de cargar datasets desde archivos CSV y de transformar los productos en vectores numéricos utilizando TF-IDF, lo que permite calcular similitudes entre ellos.

### Historial.csv, Usuarios.csv y productos.csv
En estos archivos se guardan los distintos datos que se manejan en la aplicacion.

#### Para mas detalle los codigos estan comentados 

## Como ejecutar:

Primero tiene que installar Pandas y streamlit desde terminal ingresando:
py -m ensurepip --upgrade   
py -m pip install streamlit
py -m pip install pandas    
py -m pip install scikit-learn

Y para ejecutar usara:
py -m streamlit run Main.py o py -m streamlit run interfaz.py

## Que hacer
Al ejecutar el programa se ejecutara en el navegador la interfazen la que se podra seleccionar un usuario y podras ver una pequeña lista de recomendaciones de cada usuario. 
Puedes registrar una compra. Para visualizar el cambio en las recomendaciones despues de la compra tienes que actualizar la pagina para ver los cambios en los productos recomendados, esto ultimo es mas facil de visualizar con un usuario nuevo, el cual puedes crear agregando datos en el archivo Usuarios.csv

#### Pequeña visualizacion de la interfaz 
<img width="937" height="737" alt="image" src="https://github.com/user-attachments/assets/ba48fe7f-bf55-45bc-a5be-a951c935cd7f" />

