# base_plugin.py
# Interfaz base para plugins del agente

class BasePlugin:
    def ejecutar(self, datos):
        """Método que debe implementar cada plugin para procesar datos."""
        raise NotImplementedError("El plugin debe implementar el método ejecutar.")
