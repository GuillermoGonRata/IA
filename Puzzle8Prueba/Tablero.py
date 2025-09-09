sol =  [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]

class Tablero:
    def __init__(self,nums=[[1,2,3],[4,5,6],[7,8,0]]):
        self.nums = nums 
        
    def Solucion(self):
        return self.nums == sol
    
    def vacio(self):
        for ir, r in enumerate(self.nums):
            for ic, c in enumerate(r):
                if c == 0:
                    return ir, ic
                
    def movimientos(self):
        r,c = self.vacio()
        return movimientos[r][c]          
    
    def moverse(self, dir):
        r,c = self.vacio()
        
        if dir=='l':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r][c-1]
            self.nums[r][c-1] = aux
        elif dir=='r':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r][c+1]
            self.nums[r][c+1] = aux
        elif dir=='u':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r-1][c]
            self.nums[r-1][c] = aux
        elif dir=='d':
            aux = self.nums[r][c]
            self.nums[r][c] = self.nums[r+1][c]
            self.nums[r+1][c] = aux