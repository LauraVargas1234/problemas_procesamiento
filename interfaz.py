import tkinter as tk

class InterfazSimulador:
    def __init__(self, root, gestor):
        self.root = root
        self.gestor = gestor
        self.estudiantes = ["Laura", "Diego", "Tatiana", "Julian"]
        self.recursos = list(gestor.recursos.keys())
        self.setup_ui()

    # Método para configurar la interfaz gráfica
    def setup_ui(self):
        self.text_area = tk.Text(self.root, height=20, width=85, bg="#ffffff", fg="#222222", font=("Courier", 10))
        self.text_area.pack(padx=10, pady=10)

        # Función para registrar mensajes en el área de texto
        def log(msg):
            self.text_area.insert(tk.END, msg + "\n")
            self.text_area.see(tk.END)

        self.gestor.log = log

        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack()

        tk.Label(frame, text="Estudiante:", bg="#f0f0f0").grid(row=0, column=0)
        self.est_var = tk.StringVar(value=self.estudiantes[0])
        tk.OptionMenu(frame, self.est_var, *self.estudiantes).grid(row=0, column=1)

        tk.Label(frame, text="Recurso", bg="#f0f0f0").grid(row=1, column=0)
        tk.Label(frame, text="Tiempo (s)", bg="#f0f0f0").grid(row=1, column=1)

        self.recurso_vars = {}
        self.tiempo_vars = {}

        for i, recurso in enumerate(self.recursos):
            var = tk.BooleanVar()
            tiempo = tk.Entry(frame, width=5)
            tiempo.insert(0, "10")
            self.recurso_vars[recurso] = var
            self.tiempo_vars[recurso] = tiempo
            tk.Checkbutton(frame, text=recurso, variable=var, bg="#f0f0f0").grid(row=i+2, column=0, sticky="w")
            tiempo.grid(row=i+2, column=1)

        # Botones
        tk.Button(self.root, text="Solicitar Recurso(s)", command=self.solicitar, bg="#4CAF50", fg="white").pack(pady=4)
        tk.Button(self.root, text="Ver Estado", command=self.gestor.estado_actual, bg="#2196F3", fg="white").pack(pady=4)
        tk.Button(self.root, text="Exportar Resultados", command=self.gestor.exportar_csv, bg="#FF9800", fg="white").pack(pady=4)

    # Método para manejar la solicitud de recursos
    def solicitar(self):
        estudiante = self.est_var.get()
        recursos_tiempos = {}

        # Validar que se seleccionen recursos con tiempos válidos
        for recurso, seleccionado in self.recurso_vars.items():
            if seleccionado.get():
                try:
                    tiempo = int(self.tiempo_vars[recurso].get())
                    if tiempo <= 0:
                        raise ValueError
                    recursos_tiempos[recurso] = tiempo
                except ValueError:
                    self.gestor.log(f"Tiempo inválido para {recurso}. Usa un número entero positivo.")
                    return

        # Si no hay recursos seleccionados, mostrar mensaje de error
        if not recursos_tiempos:
            self.gestor.log("Debes seleccionar al menos un recurso con tiempo válido.")
            return

        self.gestor.solicitar(estudiante, recursos_tiempos)
