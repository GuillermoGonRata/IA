import tkinter as tk
from tkinter import simpledialog, messagebox
from Nodo import Nodo, Tablero, busquedaAmplitud
import random

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
        btn_opts = {
            "font": ('Times new Roman', 24),
            "bg": 'white',
            "fg": 'blue',
            "width": 4,
            "height": 2,
            "borderwidth": 3,
            "relief": 'ridge'
        }
        if n != 0:
            self.button = tk.Button(
                self.frame, text=str(self.n),
                command=lambda: frame.master.move(self.contador, self.r, self.c),
                **btn_opts
            )
        else:
            self.button = tk.Button(
                self.frame, text='',
                command=lambda: frame.master.move(self.contador, self.r, self.c),
                **btn_opts
            )
        self.button.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        # Hace que las celdas crezcan proporcionalmente
        self.frame.grid_rowconfigure(r, weight=1)
        self.frame.grid_columnconfigure(c, weight=1)
            
            
class Frame_Tablero(tk.Frame):
    
    def busquedaAmplitud(self):
        nodo_inicial = Nodo(nums=self.aux_tablero.nums)
        camino, explorados = busquedaAmplitud(nodo_inicial)
        if camino:
            self.movimientos_label.config(text=f"Movimientos: {len(camino)-1}")
            self.nodosExplorados.config(text=f"NodosExplorados: {explorados}") 
            self.mostrarMovimientos(camino)
            messagebox.showinfo("Solución encontrada", f"Solución encontrada en {len(camino)-1} movimientos.")
        else:
            self.movimientos_label.config(text="No hay solución")
            messagebox.showinfo("Sin solución", "No hay solución para este tablero.")

    def mostrarMovimientos(self, camino, paso=0):
        if paso < len(camino):
            self.actualizar(camino[paso].Tablero.nums)
            self.after(100, lambda: self.mostrarMovimientos(camino, paso+1)) 

    def __init__(self, parent, root):
        self.root = root
        tk.Frame.__init__(self, parent, bg='gray')
        self.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Frame para el tablero
        self.tablero_frame = tk.Frame(self, bg='gray')
        self.tablero_frame.place(relx=0.1, rely=0.05, relwidth=0.8, relheight=0.6)

        b_solve = tk.Button(self, text='Resolver', command=self.busquedaAmplitud, font=('Times new Roman', 24), bg='white', fg='blue', padx=10, pady=5)
        b_solve.place(relx=0.3, rely=0.85, relwidth=0.4, relheight=0.1)

        b_nuevo = tk.Button(self, text='Nuevo Aleatorio', command=self.nuevoAleatorio, font=('Times new Roman', 14), bg='white', fg='green')
        b_nuevo.place(relx=0.05, rely=0.75, relwidth=0.20, relheight=0.08)

        b_config = tk.Button(self, text='Configurar', command=self.configurarTablero, font=('Times new Roman', 14), bg='white', fg='purple')
        b_config.place(relx=0.75, rely=0.75, relwidth=0.20, relheight=0.08)

        self.movimientos_label = tk.Label(self, text="Movimientos: 0", font=('Times new Roman', 16), bg='gray', fg='black')
        self.movimientos_label.place(relx=0.35, rely=0.70, relwidth=0.3, relheight=0.08)
        
        self.nodosExplorados = tk.Label(self, text="NodosExplorados: 0", font=('Times new Roman', 16), bg='gray', fg='black')
        self.nodosExplorados.place(relx=0.35, rely=0.75, relwidth=0.35, relheight=0.08)

        self.nums = generarTableroInicial()
        self.aux_tablero = Tablero(self.nums)

        self.fichas = []
        for ir, r in enumerate(self.nums):
            fila = []
            for ic, c in enumerate(r):
                aux = Ficha(ir, ic, c, self.tablero_frame)
                fila.append(aux)
            self.fichas.append(fila)
        self.actualizar(self.nums)

    def nuevoAleatorio(self):
        self.nums = generarTableroAleatorio()
        self.aux_tablero = Tablero(self.nums)
        self.actualizar(self.nums)
        self.movimientos_label.config(text="Movimientos: 0")

    def configurarTablero(self):
        entrada = simpledialog.askstring("Configurar tablero", "Introduce los 9 números separados por espacios (usa 0 para el espacio vacío):\nEjemplo: 1 2 3 4 5 6 7 8 0")
        if entrada:
            try:
                valores = [int(x) for x in entrada.strip().split()]
                if sorted(valores) != list(range(9)):
                    raise ValueError
                if not esResoluble(valores):
                    messagebox.showerror("No resoluble", "La configuración no es resoluble.")
                    return
                self.nums = [valores[i*3:(i+1)*3] for i in range(3)]
                self.aux_tablero = Tablero(self.nums)
                self.actualizar(self.nums)
                self.movimientos_label.config(text="Movimientos: 0")
            except Exception:
                messagebox.showerror("Error", "Entrada inválida. Debes ingresar los números del 0 al 8 sin repetir.")

    def move(self,fr, fc):
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
        for ir, r in enumerate(nums):
            for ic, c in enumerate(r):
                ficha = self.fichas[ir][ic]
                if c != 0:
                    ficha.button.config(text=str(c), background='white', fg='blue', borderwidth=3, relief='ridge')
                else:
                    ficha.button.config(text='', background='white', fg='blue', borderwidth=2, relief='ridge')
        
def esResoluble(nums_flat):
    inv = 0
    for i in range(len(nums_flat)):
        for j in range(i+1, len(nums_flat)):
            if nums_flat[i] != 0 and nums_flat[j] != 0 and nums_flat[i] > nums_flat[j]:
                inv += 1
    return inv % 2 == 0

def generarTableroAleatorio():
     nums_flat = list(range(9))
     while True:
         random.shuffle(nums_flat)
         if esResoluble(nums_flat):
             break
     # Convierte la lista plana a una matriz 3x3
     return [nums_flat[i*3:(i+1)*3] for i in range(3)]

def generarTableroInicial():
    numsFlat = [3,2,1,4,6,5,8,7,0]
    return [numsFlat[i*3:(i+1)*3] for i in range(3)]

if __name__ == '__main__':
    app = App()
    app.mainloop()