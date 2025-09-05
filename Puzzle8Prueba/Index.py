estado_inicial = [1, 2, 3,
                  4, 5, 6,
                  7, 0, 8]   # el 0 representa el espacio vacío

estado_meta = [1, 2, 3,
               4, 5, 6,
               7, 8, 0]

from collections import deque

# Estado meta
objetivo = [1,2,3,4,5,6,7,8,0]

# Movimientos posibles (arriba, abajo, izquierda, derecha)
movimientos = {
    0: [1, 3],       # desde la posición 0, puedes mover derecha o abajo
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7]
}

def mover(estado, pos_vacio, pos_nueva):
    nuevo = estado[:]
    nuevo[pos_vacio], nuevo[pos_nueva] = nuevo[pos_nueva], nuevo[pos_vacio]
    return nuevo

def bfs(inicio):
    cola = deque([(inicio, [])])
    visitados = set()

    while cola:
        estado, camino = cola.popleft()
        if estado == objetivo:
            return camino + [estado]

        pos_vacio = estado.index(0)
        for m in movimientos[pos_vacio]:
            nuevo_estado = mover(estado, pos_vacio, m)
            estado_tupla = tuple(nuevo_estado)
            if estado_tupla not in visitados:
                visitados.add(estado_tupla)
                cola.append((nuevo_estado, camino + [estado]))
    return None

# Ejemplo de ejecución
estado_inicial = [1,2,3,4,0,6,7,5,8]
solucion = bfs(estado_inicial)

print("Solución encontrada en", len(solucion)-1, "movimientos")
for paso in solucion:
    print(paso[0:3])
    print(paso[3:6])
    print(paso[6:9])
    print("----")
