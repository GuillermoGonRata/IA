from Tablero import Tablero
from copy import deepcopy

class Nodo:
    def _init_(self, father=None, nums=[],dir='l'):
        self.father = father
        if self. father is None:
            self.Tablero = Tablero(nums)
        else:
            self.Tablero = deepcopy(self.father.Tablero)
            self.Tablero.mover(dir=dir)
            
    def setChild(self):
        self.childs = []
        for _dir in self.Tablero.moves():
            auxN = Nodo(father=self, dir=_dir)
            self.childs(append(auxN))
            
            