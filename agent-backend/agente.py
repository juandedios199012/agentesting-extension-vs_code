# agente.py
# Clase principal para el agente Python

class AgentePython:
    def __init__(self):
        self.estado = "inicializado"

    def ejecutar(self):
        print(f"Agente ejecutando. Estado actual: {self.estado}")

    def detener(self):
        self.estado = "detenido"
        print("Agente detenido.")
