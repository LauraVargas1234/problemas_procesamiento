import threading
import time
import csv
import os
from recurso import Recurso

class GestorRecursos:
    def __init__(self, recursos, log_func=print):
        self.recursos = {r: Recurso(r) for r in recursos}
        self.log = log_func
        self.registro_tiempos = []
    # Método para solicitar recursos en orden
    def solicitar(self, estudiante, recursos_tiempos):
        threading.Thread(target=self._usar_recursos_en_orden, args=(estudiante, recursos_tiempos), daemon=True).start()

    # Método para gestionar el uso de recursos
    def _usar_recursos_en_orden(self, estudiante, recursos_tiempos):
        for recurso_nombre, tiempo_total in recursos_tiempos.items():
            
            recurso = self.recursos[recurso_nombre]
            tiempo_restante = tiempo_total

            # Si el recurso está ocupado, el estudiante espera en la cola
        
            while tiempo_restante > 0:
                recurso.cola_espera.put(estudiante)
                tiempo_inicio = time.time()
                self.log(f"→ {estudiante} solicitó el recurso: {recurso_nombre} (le quedan {tiempo_restante}s)")

                # Espera hasta que el estudiante esté al frente de la cola
                while recurso.cola_espera.queue[0] != estudiante:
                    time.sleep(0.1)

                recurso.semaforo.acquire()
                recurso.cola_espera.get()
                recurso.estado = estudiante

                # Calcula el tiempo de espera
                tiempo_espera = time.time() - tiempo_inicio
                tiempo_uso = min(10, tiempo_restante)
                self.log(f"✔ {estudiante} usando {recurso_nombre} por {tiempo_uso}s (esperó {tiempo_espera:.2f}s)")

                # Simula el uso del recurso
                time.sleep(tiempo_uso)
                tiempo_restante -= tiempo_uso

                recurso.estado = None
                recurso.semaforo.release()

                # Registra el tiempo de uso y espera
                self.registro_tiempos.append({
                    "estudiante": estudiante,
                    "recurso": recurso_nombre,
                    "espera_segundos": round(tiempo_espera, 2),
                    "uso_segundos": tiempo_uso,
                    "control": True
                })

                # Verifica si el estudiante terminó de usar el recurso
                if tiempo_restante == 0:
                    self.log(f"✘ {estudiante} completó el uso de {recurso_nombre}")
                else:
                    self.log(f"↺ {estudiante} vuelve a la cola de {recurso_nombre} (faltan {tiempo_restante}s)")

    # Método para mostrar el estado actual de los recursos
    def estado_actual(self):
        self.log("------ ESTADO DE LOS RECURSOS ------")
        for r in self.recursos.values():
            ocupante = r.estado or "LIBRE"
            esperando = list(r.cola_espera.queue)
            self.log(f"{r.nombre}: {ocupante} | Esperando: {esperando}")
        self.log("------------------------------------")

    # Método para exportar los registros a un archivo CSV
    def exportar_csv(self):
        os.makedirs("resultados", exist_ok=True)
        path = "resultados/resultados_con_control.csv"
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["estudiante", "recurso", "espera_segundos", "uso_segundos", "control"])
            writer.writeheader()
            writer.writerows(self.registro_tiempos)
        self.log(f"Registros exportados a {path}")
