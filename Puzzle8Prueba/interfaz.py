import tkinter as tk
from Nodo import Nodo,Tablero,solve

moves=  [[1,3],[0,2,4],[1,5],
               [0,4,6],[1,3,5,7],[2,4,8],
               [3,7],[4,6,8],[5,7]]

class App(tk.Tk):
    def __init__(self, * args, **kargs):
        tk.Tk.__init__(self, *args, **kargs)
        self.geometry('650x600')
        self.container = tk.Frame(self,bg='red')
        self.container.place(relx=0,rely=0,relwidth=1,relheight=1)
        fTab = Frame_Tablero(self.container,self)
        fTab.tkraise()
        
class Ficha:
    contador = 0
    def __init__(self, r, c, n, frame, mover_callback=None):
        self.frame = frame
        self.r = r
        self.c = c
        self.n = n
        self.contador = Ficha.contador
        Ficha.contador +=  1
        if n != 0:
            self.button = tk.Button(self.frame, text=str(self.n), font=('Times new Roman', 42),  bg='white', fg='blue', command=lambda: frame.move(self.contador, self.r, self.c))
            self.button.place(relx=1/26+self.c*(4/13), rely= 0.05+self.r*(1/4), relheight=1/4, relwidth=4/13)
        else:
            self.button = tk.Button(self.frame, text='',  font=('Times new Roman', 42),bg='white', fg='blue', command=lambda: frame.move(self.contador,self.r, self.c))
            self.button.place(relx=1/26+self.c*(4/13), rely= 0.05+self.r*(1/4), relheight=1/4, relwidth=4/13)   
            
            
class Frame_Tablero(tk.Frame):
    
    def solve(self):
        nodo_inicial = Nodo(nums=self.aux_tablero.nums)
        camino = solve(nodo_inicial)
        if camino:
            print("Solución encontrada con", len(camino)-1, "movimientos")
            self.showAdvance(camino)
        else:
            print("No hay solución para este tablero")

    def showAdvance(self, camino, paso=0):
        if paso < len(camino):
            self.actualizar(camino[paso].Tablero.nums)
            self.after(100, lambda: self.showAdvance(camino, paso+1)) 

    def __init__(self, parent, root):
        self.root = root
        tk.Frame.__init__(self, parent, bg='gray')
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        b_solve = tk.Button(self, text='Resolver', command=lambda:self.solve(), font=('Times new Roman', 42), bg='white', fg='blue',padx=40,pady=20)
        b_solve.place(relx=0.3, rely=0.85, relwidth=0.4, relheight=0.1)
        self.nums = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.aux_tablero = Tablero(self.nums)
        
        
        self.fichas = []
        for ir, r in enumerate(self.nums):
            for ic, c in enumerate(r):
                aux = Ficha(ir, ic, c, self)
                self.fichas.append(aux)
            
                
    # Mover fichas
    def move(self, icontador, fr, fc):
        er, ec = self.aux_tablero.empty()
        ficha_idx = fr * 3 + fc
        vacio_idx = er * 3 + ec
        auxm = None
        if vacio_idx in moves[ficha_idx]:
            if er == fr:
                auxm = 'l' if fc < ec else 'r'
            else:
                auxm = 'u' if fr < er else 'd'
        if auxm:
            self.aux_tablero.makeMove(auxm)
            self.actualizar(self.aux_tablero.nums)
        
    def actualizar(self, nums):
        aux = 0
        for ir, r in enumerate(nums):
            for ic,c in enumerate(r):
                if c != 0:
                    self.fichas[aux].button.config(text=str(c),background='white',fg='blue',borderwidth=10,relief='raised')
                else:
                    self.fichas[aux].button.config(text='',background='white',fg='blue', borderwidth=2,relief='raised')
                aux += 1
        
        
if __name__ == '__main__':
    app = App()
    app.mainloop()