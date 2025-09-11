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

def solve(root):
    sol= busquedaAmplitud(root)
    camino = []
    aux = sol
    while True:
        camino.insert(0,aux)
        aux = aux.father
        if aux == None:
            break
    return camino
    