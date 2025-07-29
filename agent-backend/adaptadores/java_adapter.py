# java_adapter.py
# Adaptador para analizar proyectos Java
import os

class JavaAdapter:
    def __init__(self, ruta):
        self.ruta = ruta

    def analizar_estructura(self):
        print(f"Analizando proyecto Java en: {self.ruta}")
        archivos = []
        for root, dirs, files in os.walk(self.ruta):
            for file in files:
                if file.endswith('.java'):
                    archivos.append(os.path.join(root, file))
        print(f"Archivos Java encontrados: {len(archivos)}")
        return archivos
