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
   
            
    def set_childs(self):
        self.childs = []
        for _dir in self.Tablero.moves():
            auxN = Nodo(father=self, dir=_dir)
            self.childs.append(auxN)
            
    def generar_hijos(self):
        hijos = []
        for _dir in self.Tablero.moves():
            hijo = Nodo(father=self, dir=_dir)
            hijos.append(hijo)
        return hijos
   
def is_in(lista, elemento):
    for x in lista:
        if x == elemento:
            return True
    return False

def busquedaAmplitud(root):
    x = [root]
    visitados = []
    it  = 0
    while x:
        it +=1
        if x[0].Tablero.isSolution():
            print('Nodos recorridos',it)
            return x[0]
        else:
            x[0].set_childs()
            auxChilds = x[0].childs
            visitados.append(x[0].Tablero.nums)
            x.pop(0)
            for ci in auxChilds:
                if not is_in(visitados,ci.Tablero.nums):
                    x += [ci]
            print('Movimientos: ',it,' Nodos por visitar: ',len(x),' Visitados: ',len(visitados))
    print("No hay solución.")
    return None

def solve(nodo_inicial):
    from collections import deque
    visitados = set()
    cola = deque()
    cola.append((nodo_inicial, []))
    while cola:
        nodo, camino = cola.popleft()
        estado = tuple(sum(nodo.Tablero.nums, []))  # Convierte la matriz a tupla plana
        if estado in visitados:
            continue
        visitados.add(estado)
        if nodo.Tablero.isSolution():  # Cambiado a isSolution
            return camino + [nodo]
        for hijo in nodo.generar_hijos():  # Usar el nuevo método
            cola.append((hijo, camino + [nodo]))
    return None
