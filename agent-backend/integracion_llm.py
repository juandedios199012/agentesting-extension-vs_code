"""
integracion_llm.py
Módulo para integración con modelos de lenguaje (LLM) como OpenAI GPT.
"""
import requests
from logger import log_event
from config_secreta import get_llm_credentials

class LLMClient:
    def __init__(self):
        creds = get_llm_credentials()
        self.api_key = creds['api_key']
        self.api_url = creds['api_url']

    def analizar_historia(self, historia_usuario):
        """
        Envía la historia de usuario al LLM y retorna sugerencias de escenarios y steps.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "prompt": f"Analiza la siguiente historia de usuario y sugiere escenarios y steps en formato Cucumber.\nHistoria: {historia_usuario}",
            "max_tokens": 512
        }
        try:
            response = requests.post(self.api_url, json=data, headers=headers)
            if response.status_code == 200:
                resultado = response.json().get('choices', [{}])[0].get('text', '')
                log_event("Respuesta LLM recibida", "INFO")
                return resultado
            else:
                log_event(f"Error LLM: {response.text}", "ERROR")
        except Exception as e:
            log_event(f"Excepción LLM: {e}", "ERROR")
        return None
