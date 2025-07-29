# ejemplo_plugin.py
# Ejemplo de plugin que extiende BasePlugin
from plugins.base_plugin import BasePlugin

class EjemploPlugin(BasePlugin):
    def ejecutar(self, datos):
        print(f"[PLUGIN] Procesando datos: {datos}")
        return f"Resultado del plugin para: {datos}"
