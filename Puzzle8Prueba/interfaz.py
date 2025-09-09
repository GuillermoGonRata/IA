import tkinter as tk
from Nodo import Nodo,Tablero

movimientos=  [[1,3],[0,2,4],[1,5],
               [0,4,6],[1,3,5,7],[2,4,8],
               [3,7],[4,6,8],[5,7]]

class App(tk.Tk):
    def __init__(self, * args, **kargs):
        tk.Tk.__init__(self, *args, **kargs)
        self.geometry('650x800')
        self.container = tk.Frame(self,bg='red')
        self.container.place(relx=0,rely=0,relwidth=1,relheight=1)
        fTab = Frame_Tablero(self.container,self)
        fTab.tkraise()
        
class Ficha:
    cont = 0
    def __init__(self, r, c, n, frame, mover_callback=None):
        self.frame = frame
        self.r = r
        self.c = c
        self.n = n
        self.cont = Ficha.cont
        Ficha.cont += 1
        if n != 0:
            self.boton = tk.Button(
                self.frame,
                text=str(self.n),
                font=('Times new Roman', 24),
                bg='white',
                fg='black',
                command=lambda: mover_callback(self.cont, self.r, self.c) if mover_callback else None
            )
            self.boton.place(relx=c*0.33, rely=r*0.33, relwidth=0.33, relheight=0.33)
        else:
            self.boton = tk.Button(
                self.frame,
                text='',
                font=('Times new Roman', 24),
                bg='white',
                fg='black',
                command=lambda: mover_callback(self.cont, self.r, self.c) if mover_callback else None
            )
            self.boton.place(relx=c*0.33, rely=r*0.33, relwidth=0.33, relheight=0.33)
            
            
class Frame_Tablero(tk.Frame):
    def __init__(self, parent, root):
        self.root = root
        tk.Frame.__init__(self, parent, bg='blue')
        self.place(relx=0, rely=0, relwidth=1, relheight=1)
        b_resuelve = tk.Button(self, text='Resolver', font=('Times new Roman', 24), bg='white', fg='black', command=self.solucion)
        b_resuelve.place(relx=0.1, rely=0.9, relwidth=0.3, relheight=0.1)
        b_nums = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        self.aux_tablero = Tablero(b_nums)
        self.fichas = []
        for ir, r in enumerate(b_nums):
            for ic, c in enumerate(r):
                aux = Ficha(ir, ic, c, self, self.mover)
                self.fichas.append(aux)
                
    def solucion(self):
        pass
                
    # Mover fichas
    def mover(self, icont, fr, fc):
        er, ec = self.aux_tablero.vacio()
        ficha_idx = fr * 3 + fc
        vacio_idx = er * 3 + ec
        auxm = None
        if vacio_idx in movimientos[ficha_idx]:
            if er == fr:
                auxm = 'l' if fc < ec else 'r'
            else:
                auxm = 'u' if fr < er else 'd'
        if auxm:
            self.aux_tablero.moverse(auxm)
            self.actualizar(self.aux_tablero.nums)
        
    def actualizar(self, nums):
        aux = 0
        for ir, r in enumerate(nums):
            for ic,c in enumerate(r):
                if c != 0:
                    self.fichas[aux].boton.config(text=str(c),background='black',fg='white',borderwidth=10,relief='raised')
                else:
                    self.fichas[aux].boton.config(text='',background='white', borderwidth=2,relief='sunken')
                aux += 1
        
        
if __name__ == '__main__':
    app = App()
    app.mainloop()