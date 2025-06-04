import tkinter as tk
from gestor import GestorRecursos
from interfaz import InterfazSimulador

# Recursos disponibles
recursos = ["Osciloscopio", "Computador", "Laboratorio", "Microscopio"]
gestor = GestorRecursos(recursos)

root = tk.Tk()
root.title("Simulación CON Control de Recursos")
InterfazSimulador(root, gestor)
root.mainloop()
