import tkinter as tk
from tkinter import messagebox

# Estado inicial y meta
estado = [1, 2, 3,
          4, 0, 5,
          6, 7, 8]

objetivo = [1, 2, 3,
            4, 5, 6,
            7, 8, 0]

# Función para actualizar botones
def actualizar_tablero():
    for i in range(9):
        if estado[i] == 0:
            botones[i].config(text="", bg="lightgray")
        else:
            botones[i].config(text=str(estado[i]), bg="white")

# Mover ficha si es posible
def mover(i):
    pos_vacio = estado.index(0)
    fila_v, col_v = divmod(pos_vacio, 3)
    fila_i, col_i = divmod(i, 3)

    # Solo se puede mover si está al lado del vacío
    if abs(fila_v - fila_i) + abs(col_v - col_i) == 1:
        estado[pos_vacio], estado[i] = estado[i], estado[pos_vacio]
        actualizar_tablero()
        if estado == objetivo:
            messagebox.showinfo("¡Ganaste!", "Has resuelto el puzzle 🎉")

# Crear ventana
ventana = tk.Tk()
ventana.title("Puzzle 8")

# Crear botones
botones = []
for i in range(9):
    b = tk.Button(ventana, text=str(estado[i]) if estado[i] != 0 else "",
                  width=5, height=2, font=("Arial", 20),
                  command=lambda i=i: mover(i))
    b.grid(row=i//3, column=i%3, padx=5, pady=5)
    botones.append(b)

actualizar_tablero()

ventana.mainloop()
