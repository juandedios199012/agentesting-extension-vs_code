# integracion_proyectos.py
# Clase base para integración de proyectos de automatización

class IntegracionProyecto:
    def __init__(self, ruta):
        self.ruta = ruta

    def analizar_estructura(self):
        raise NotImplementedError("Este método debe ser implementado por el adaptador específico.")

# Ejemplo de uso con adaptador Java
from adaptadores.java_adapter import JavaAdapter

# Para usar:
# java = JavaAdapter(ruta)
# java.analizar_estructura()
