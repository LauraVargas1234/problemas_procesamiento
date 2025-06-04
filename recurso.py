from queue import Queue
import threading

class Recurso:
    def __init__(self, nombre):
        self.nombre = nombre
        self.semaforo = threading.Semaphore(1)
        self.estado = None
        self.cola_espera = Queue()
