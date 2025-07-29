# logger.py
# Registro de eventos para el agente Python
import datetime
import os
from config import CONFIG

LOG_FILE = CONFIG.get("LOG_FILE", "agente.log")

def log_event(mensaje, nivel="INFO"):
    tiempo = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{tiempo}] [{nivel}] {mensaje}"
    print(log_line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"[ERROR] No se pudo escribir en el archivo de log: {e}")
