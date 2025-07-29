# errores.py
# Manejo básico de errores para el agente Python

class ErrorAgente(Exception):
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje
