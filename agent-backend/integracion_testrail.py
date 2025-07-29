"""
integracion_testrail.py
Ejemplo de integración para exportar features a TestRail usando configuración segura.
"""
import requests
from logger import log_event
from config_secreta import get_testrail_credentials

class TestRailExporter:
    def __init__(self):
        creds = get_testrail_credentials()
        self.url = creds['url']
        self.usuario = creds['user']
        self.token = creds['token']

    def exportar_feature(self, proyecto_id, titulo, descripcion):
        endpoint = f"{self.url}/index.php?/api/v2/add_case/{proyecto_id}"
        headers = {"Content-Type": "application/json"}
        auth = (self.usuario, self.token)
        data = {
            "title": titulo,
            "custom_description": descripcion
        }
        try:
            response = requests.post(endpoint, json=data, headers=headers, auth=auth)
            if response.status_code == 200:
                log_event(f"Feature exportado a TestRail: {titulo}", "INFO")
                return response.json()
            else:
                log_event(f"Error al exportar a TestRail: {response.text}", "ERROR")
        except Exception as e:
            log_event(f"Excepción al exportar a TestRail: {e}", "ERROR")
        return None
