# GUIPrincipal.py
import tkinter as tk
from Frontend import logica

ventana = tk.Tk()
ventana.title("Estacionamiento Inteligente")
ventana.geometry("400x300")

resultado = tk.StringVar()
historial_texto = tk.StringVar()

estados_botones = {}

def refrescar():
    logica.actualizar_visual(estados_botones)
    ventana.after(2000,refrescar)

refrescar()

logica.borrar_historial()

tk.Label(ventana, text="Sistema de Estacionamiento").pack(pady=10)
botonReg = tk.Button(ventana, text="Registrar acceso", command=lambda: logica.registrar(resultado, ventana)).pack(pady=5)
tk.Label(ventana, textvariable=resultado, fg="blue", wraplength=350).pack(pady=10)
tk.Button(ventana,text="Ver historial", command=lambda: logica.mostrar_historial(historial_texto)).pack(pady=5)
tk.Label(ventana, text="Historial entradas:").pack()
tk.Label(ventana, textvariable=historial_texto, justify="left").pack()

frame_espacios = tk.Frame(ventana)
frame_espacios.pack(pady=10)

for etiqueta in ['A','B','C']:
    boton = tk.Button(frame_espacios, text=etiqueta, width=10, height=2, bg="gray")
    boton.grid(row=0, column=['A','B','C'].index(etiqueta),padx=5)
    estados_botones[etiqueta] = boton


ventana.mainloop()
