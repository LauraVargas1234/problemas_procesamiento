import tkinter as tk
import threading
import time
import csv
import os

# Recursosy estudiantes
recursos = ["Osciloscopio", "Computador", "Laboratorio", "Microscopio"]
estado_recursos = {r: None for r in recursos}
cola_espera_simulada = {r: [] for r in recursos} 
estudiantes = ["Laura", "Diego", "Tatiana", "Julian"]

# Lista para guardar tiempos de espera
registro_tiempos = []

# Crear ventana
root = tk.Tk()
root.title("Simulación SIN Control - Registro de Tiempos")
root.configure(bg="#f0f0f0")

# Área de texto para mostrar los eventos
text_area = tk.Text(root, height=18, width=80, bg="#ffffff", fg="#222222", font=("Courier", 10))
text_area.pack(padx=10, pady=10)

# Frame para controles
frame_controls = tk.Frame(root, bg="#f0f0f0")
frame_controls.pack(pady=5)

# Función para mostrar eventos en pantalla
def log(msg):
    text_area.insert(tk.END, f"{msg}\n")
    text_area.see(tk.END)

# Hilo por solicitud sin control de concurrencia
def intentar_ocupar(estudiante, recurso):
    tiempo_inicio = time.time()
    log(f"→ {estudiante} solicita el recurso: {recurso}")

    ya_agregado = False
    while estado_recursos[recurso] is not None:
        if not ya_agregado and estudiante not in cola_espera_simulada[recurso]:
            cola_espera_simulada[recurso].append(estudiante)
            ya_agregado = True
        time.sleep(0.1)

    # Al liberar el recurso, se elimina de la cola de espera
    if estudiante in cola_espera_simulada[recurso]:
        cola_espera_simulada[recurso].remove(estudiante)

    tiempo_total = time.time() - tiempo_inicio
    estado_recursos[recurso] = estudiante
    log(f"✔ {recurso} ha sido ocupado por {estudiante} tras esperar {tiempo_total:.2f} segundos")

    registro_tiempos.append({
        "estudiante": estudiante,
        "recurso": recurso,
        "espera_segundos": round(tiempo_total, 2),
        "control": False
    })

# Función para solicitar recurso
def solicitar():
    estudiante = estudiante_var.get()
    recurso = recurso_var.get()
    threading.Thread(target=intentar_ocupar, args=(estudiante, recurso), daemon=True).start()

# Acción para liberar recurso manualmente
def liberar():
    recurso = recurso_var.get()
    ocupante = estado_recursos.get(recurso)
    if ocupante:
        estado_recursos[recurso] = None
        log(f"✘ {recurso} ha sido liberado por {ocupante}")
    else:
        log(f"{recurso} ya está libre")

# Ver el estado actual de los recursos y su cola
def estado_actual():
    log("------ ESTADO DE LOS RECURSOS ------")
    for r in recursos:
        ocupante = estado_recursos[r]
        if ocupante:
            log(f"{r}: El recurso esta ocupado por {ocupante}")
        else:
            log(f"{r}: El recurso esta libre")  

        if cola_espera_simulada[r]:
            log(f"El recurso esta siendo esperado por: {cola_espera_simulada[r]}")
        else:
            log(f"El recurso esta siendo esperado por: []")
    log("------------------------------------")

# Exportar los registros a archivo CSV
def exportar_registros():
    output_folder = "resultados"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "resultados_sin_control.csv")

    with open(output_path, "w", newline='') as csvfile:
        fieldnames = ["estudiante", "recurso", "espera_segundos", "control"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(registro_tiempos)

    log(f"Registros exportados a {output_path}")

# Menús desplegables
tk.Label(frame_controls, text="Estudiante:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
estudiante_var = tk.StringVar(root)
estudiante_var.set(estudiantes[0])
tk.OptionMenu(frame_controls, estudiante_var, *estudiantes).grid(row=0, column=1, padx=5)

tk.Label(frame_controls, text="Recurso:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
recurso_var = tk.StringVar(root)
recurso_var.set(recursos[0])
tk.OptionMenu(frame_controls, recurso_var, *recursos).grid(row=0, column=3, padx=5)

# Botones principales
tk.Button(frame_controls, text="Solicitar Recurso", command=solicitar, bg="#4CAF50", fg="white").grid(row=1, column=0, columnspan=2, pady=8)
tk.Button(frame_controls, text="Liberar Recurso", command=liberar, bg="#F44336", fg="white").grid(row=1, column=2, columnspan=2, pady=8)
tk.Button(root, text="Ver Estado de Recursos", command=estado_actual, bg="#2196F3", fg="white").pack(pady=5)
tk.Button(root, text="Exportar Resultados", command=exportar_registros, bg="#FF9800", fg="white").pack(pady=5)

# Iniciar ventana
root.mainloop()
