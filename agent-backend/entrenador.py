# entrenador.py
# Módulo para entrenar el agente con el proyecto base de automatización

from logger import log_event

class EntrenadorAgente:
    def __init__(self, ruta_proyecto):
        self.ruta_proyecto = ruta_proyecto
        self.modelo = None

    def analizar_proyecto(self):
        import os
        import re
        log_event(f"Analizando y entrenando con el proyecto: {self.ruta_proyecto}", "INFO")
        clases = []
        metodos_test = []
        descripciones = []
        for root, dirs, files in os.walk(self.ruta_proyecto):
            for file in files:
                if file.endswith('.java'):
                    ruta_archivo = os.path.join(root, file)
                    try:
                        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
                            contenido = f.read()
                            # Buscar clases
                            clases_encontradas = re.findall(r'class\s+(\w+)', contenido)
                            clases.extend(clases_encontradas)
                            # Buscar métodos de prueba (anotados con @Test)
                            metodos = re.findall(r'@Test[\s\S]*?void\s+(\w+)\s*\(', contenido)
                            metodos_test.extend(metodos)
                            # Buscar comentarios Javadoc antes de métodos de prueba
                            comentarios = re.findall(r'/\*\*([\s\S]*?)\*/[\s\n\r]*@Test[\s\S]*?void\s+(\w+)\s*\(', contenido)
                            for comentario, metodo in comentarios:
                                descripcion = comentario.replace('*', '').strip().replace('\n', ' ')
                                descripciones.append({'metodo': metodo, 'descripcion': descripcion})
                        log_event(f"Archivo analizado: {ruta_archivo}", "INFO")
                    except Exception as e:
                        log_event(f"No se pudo analizar el archivo {ruta_archivo}: {e}", "ERROR")
        log_event(f"Clases encontradas: {clases}", "INFO")
        log_event(f"Métodos de prueba encontrados: {metodos_test}", "INFO")
        log_event(f"Descripciones de métodos de prueba: {descripciones}", "INFO")
        self.modelo = {
            'clases': clases,
            'metodos_test': metodos_test,
            'descripciones': descripciones
        }

    def entrenar(self):
        # Entrenamiento del agente usando la información extraída
        print("Entrenando agente...")
        pass
