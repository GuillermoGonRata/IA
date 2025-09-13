
# Puzzle 8 

Prueba nuestro algoritmo de busqueda en amplitrud para resolver el juego de puzzle 8
## Hecho por:
Gonzalez cardenas Guillermo #22170672
Urias Lugo Guillermo #22170838

## Getting Started
# Archivos
 ## Clase tablero
 Fuera de la clase tablero se encuentran las variables sol y movs_list las cuales son una matriz de 3X3 con el estado de resolucion del tablero y los posibles movimientos que se pueden realizar desde una posicion de la matriz, respectivamente.
    - Dentro de este del metodo __init__ de la clase tablero se crea la matriz de 3X3 que representa al tablero  
    - Contiene el metodo isSolution el cual se encarga de corroborar que la matriz este ordenada correctamende de acuerdo a la variable sol, la cual contiene el orden que debe tener la matriz.
    - Despues tenemos al metodo empty (vacio) el cual busca en la matriz la posicion en la cual se encuentra el numero 0 (el cual representa al vacio) y retorna la posicion en la que se encuentra.
    - El metodo moves Usa la posicion del 0, para consultar en moves_List los movimientos que se pueden realizar y retornar una lista de valores tipo char que indican que direccion pueden tomar
    - Y finalmente el metodo makeMove crea una variable llamada dir, la cual le dice al tablero que direccion puede tomar el espacio vacio e intercambiar de posicion con un numero.
 ## Clase Nodo
     
- [Clase Interfaz] (#instalación)





## Uso
1. Instrucciones sobre cómo ejecutar la aplicación:
    Para poder ejecutar nuestro puzzle 8, solo necesitara ejecutar el programa "interfaz.py"
2. Al ejecutarla ya se le dara una seed con un tablero de numeros revueltos que el algoritmo intentara resolver.
3. A su vez, puede pedirle que cree una semilla de manera aleatoria si es que quiere que resuelva una diferente o bien
   puede darle una configuracion a su gusto 





