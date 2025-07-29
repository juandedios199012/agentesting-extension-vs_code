"""
integracion_jira.py
Ejemplo de integración para exportar features a Jira usando credenciales seguras.
"""
import requests
from logger import log_event
from config_secreta import get_jira_credentials

class JiraExporter:
    def __init__(self):
        creds = get_jira_credentials()
        self.url = creds['url']
        self.usuario = creds['user']
        self.token = creds['token']

    def exportar_feature(self, proyecto, resumen, descripcion):
        endpoint = f"{self.url}/rest/api/2/issue"
        headers = {"Content-Type": "application/json"}
        auth = (self.usuario, self.token)
        data = {
            "fields": {
                "project": {"key": proyecto},
                "summary": resumen,
                "description": descripcion,
                "issuetype": {"name": "Test"}
            }
        }
        try:
            response = requests.post(endpoint, json=data, headers=headers, auth=auth)
            if response.status_code == 201:
                log_event(f"Feature exportado a Jira: {resumen}", "INFO")
                return response.json()
            else:
                log_event(f"Error al exportar a Jira: {response.text}", "ERROR")
        except Exception as e:
            log_event(f"Excepción al exportar a Jira: {e}", "ERROR")
        return None
