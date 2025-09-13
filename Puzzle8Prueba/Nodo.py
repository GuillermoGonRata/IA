from Tablero import Tablero
from copy import deepcopy

class Nodo:
    def __init__(self, father=None, nums=None, dir='l'):
        if nums is None:
            nums = [[1,2,3],[4,5,6],[7,8,0]]
        self.father = father
        if self.father is None:
            self.Tablero = Tablero(nums)
        else:
            self.Tablero = deepcopy(self.father.Tablero)
            self.Tablero.makeMove(dir=dir)
   
            
    def generarHijos(self):
        self.hijos = []
        for _dir in self.Tablero.moves():
            hijo = Nodo(father=self, dir=_dir)
            self.hijos.append(hijo)
        return self.hijos
            
   
def estaEn(lista, elemento):
    for x in lista:
        if x == elemento:
            return True
    return False

def busquedaAmplitud(nodo_inicial):
    from collections import deque
    visitados = set()  #Guarda los estados visitados para nminimizar repeticiones
    cola = deque()
    cola.append((nodo_inicial, []))
    contExp = 0  # Contador de nodos explorados
    while cola:
        nodo, camino = cola.popleft()
        estado = tuple(sum(nodo.Tablero.nums, []))  # Convierte la matriz a tupla plana
        if estado in visitados:
            continue
        visitados.add(estado)
        contExp += 1  
        if nodo.Tablero.isSolution():
            return camino + [nodo], contExp
        for hijo in nodo.generarHijos():  
            cola.append((hijo, camino + [nodo]))
    return None,contExp
