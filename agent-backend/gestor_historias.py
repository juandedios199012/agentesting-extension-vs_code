import importlib
import sys
# Descubrimiento y ejecución de plugins
def ejecutar_plugins(datos):
    import os
    plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')
    sys.path.append(plugins_dir)
    for archivo in os.listdir(plugins_dir):
        if archivo.endswith('_plugin.py') and archivo != 'base_plugin.py':
            nombre_modulo = archivo[:-3]
            try:
                modulo = importlib.import_module(nombre_modulo)
                for nombre_clase in dir(modulo):
                    clase = getattr(modulo, nombre_clase)
                    if isinstance(clase, type) and hasattr(clase, 'ejecutar'):
                        instancia = clase()
                        resultado = instancia.ejecutar(datos)
                        from logger import log_event
                        log_event(f"Plugin {nombre_clase} ejecutado. Resultado: {resultado}", "INFO")
            except Exception as e:
                from logger import log_event
                log_event(f"Error al ejecutar plugin {nombre_modulo}: {e}", "ERROR")
# gestor_historias.py
# Módulo para gestionar múltiples historias de usuario y generar escenarios
import os
from generador_cucumber import GeneradorCucumber
from logger import log_event
from config import CONFIG

import glob
def cargar_historias(ruta_carpeta=None):
    historias = []
    ruta = ruta_carpeta or CONFIG.get("CARPETA_HISTORIAS", "src/test/resources")
    patrones = ["*.txt", "*.feature", "*.java", "*.karate", "*.story"]
    archivos = []
    for patron in patrones:
        archivos.extend(glob.glob(os.path.join(ruta, "**", patron), recursive=True))
    if not archivos:
        log_event("No se encontraron archivos relevantes en la carpeta.", "WARNING")
        return historias
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                historias.append({'nombre': os.path.relpath(archivo, ruta), 'contenido': f.read()})
            log_event(f"Archivo relevante cargado: {archivo}", "INFO")
        except Exception as e:
            log_event(f"No se pudo leer el archivo {archivo}: {e}", "ERROR")
    return historias

def generar_artefactos_para_historias(ruta_carpeta=None, ruta_salida=None, llm=None, historia_caso=None, ruta_workspace=None):
    salida = ruta_salida or CONFIG.get("CARPETA_SALIDA", "src/test/generated")
    historias = []
    # Workspace global
    if ruta_workspace:
        import glob
        patrones = ["*.txt", "*.feature", "*.java", "*.karate", "*.story"]
        archivos = []
        for patron in patrones:
            archivos.extend(glob.glob(os.path.join(ruta_workspace, "**", patron), recursive=True))
        if not archivos:
            log_event("No se encontraron archivos relevantes en el workspace.", "WARNING")
        for archivo in archivos:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    historias.append({'nombre': os.path.relpath(archivo, ruta_workspace), 'contenido': f.read()})
                log_event(f"Archivo relevante cargado: {archivo}", "INFO")
            except Exception as e:
                log_event(f"No se pudo leer el archivo {archivo}: {e}", "ERROR")
    # Carpeta tradicional
    elif ruta_carpeta:
        historias = cargar_historias(ruta_carpeta)
    # Caso individual
    elif historia_caso:
        historias = [historia_caso]
    # Procesar historias
    for historia in historias:
        conocimiento = {
            'descripciones': [{'metodo': historia['nombre'], 'descripcion': historia['contenido']}],
            'metodos_test': [historia['nombre']]
        }
        generador = GeneradorCucumber(conocimiento)
        features = generador.generar_feature(historia['nombre'])
        steps = generador.generar_step_definitions(historia['nombre'])
        # Enriquecer con LLM (OpenAI)
        if llm:
            try:
                respuesta_llm = llm.analizar_historia(historia['contenido'])
                if respuesta_llm:
                    print(f"ARCHIVO: {historia['nombre']}_llm.txt\nCONTENIDO:\n{respuesta_llm}\n")
                    nombre_base = historia['nombre']
                    with open(os.path.join(salida, f"{nombre_base}_llm.txt"), 'w', encoding='utf-8') as f:
                        f.write(respuesta_llm)
                    log_event(f"Archivo enriquecido por LLM generado: {nombre_base}_llm.txt", "INFO")
            except Exception as e:
                log_event(f"No se pudo enriquecer la historia con LLM: {e}", "ERROR")
        # Guardar archivos generados y mostrar en formato estándar
        try:
            for idx, feature in enumerate(features):
                nombre_feature = f"{historia['nombre'].replace('.txt','').replace('.feature','')}_gen{idx+1}.feature"
                print(f"ARCHIVO: {nombre_feature}\nCONTENIDO:\n{feature}\n")
                with open(os.path.join(salida, nombre_feature), 'w', encoding='utf-8') as f:
                    f.write(feature + '\n')
            log_event(f"Archivo feature generado: {nombre_feature}", "INFO")
        except Exception as e:
            log_event(f"No se pudo generar el archivo feature para {historia['nombre']}: {e}", "ERROR")
        try:
            for idx, step in enumerate(steps):
                nombre_step = f"{historia['nombre'].replace('.txt','').replace('.feature','')}_gen{idx+1}_steps.java"
                print(f"ARCHIVO: {nombre_step}\nCONTENIDO:\n{step}\n")
                with open(os.path.join(salida, nombre_step), 'w', encoding='utf-8') as f:
                    f.write(step + '\n')
            log_event(f"Archivo steps generado: {nombre_step}", "INFO")
        except Exception as e:
            log_event(f"No se pudo generar el archivo steps para {historia['nombre']}: {e}", "ERROR")
