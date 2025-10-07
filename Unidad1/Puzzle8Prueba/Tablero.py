sol =  [[1, 2, 3],[4, 5, 6],[7, 8, 0]]
listaMovimientos = [[['r','d'],['l','r','d'],['l','d']], # Up, Down, Right, Left
                    [['r','u','d'],['l','r','u','d'],['l','u','d']],
                    [['u','r'],['l','u','r'],['l','u']]]

class Tablero:
    def __init__(self,nums=[[1,2,3],[4,5,6],[7,8,0]]):
        self.nums = nums 
        
    def isSolution(self):
        return self.nums == sol
    
    def empty(self):
        for ir, i in enumerate(self.nums):
            for ic, j in enumerate(i):
                if j == 0:
                    return ir, ic
                
    def moves(self):
        i,j = self.empty()
        return listaMovimientos[i][j]          
    
    def makeMove(self, dir):
        i,j = self.empty()
        
        if dir=='l':
            aux = self.nums[i][j]
            self.nums[i][j] = self.nums[i][j-1]
            self.nums[i][j-1] = aux
        elif dir=='r':
            aux = self.nums[i][j]
            self.nums[i][j] = self.nums[i][j+1]
            self.nums[i][j+1] = aux
        elif dir=='u':
            aux = self.nums[i][j]
            self.nums[i][j] = self.nums[i-1][j]
            self.nums[i-1][j] = aux
        elif dir=='d':
            aux = self.nums[i][j]
            self.nums[i][j] = self.nums[i+1][j]
            self.nums[i+1][j] = aux