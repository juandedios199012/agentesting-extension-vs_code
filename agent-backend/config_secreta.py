"""
config_secreta.py
Carga y expone credenciales y configuraciones sensibles usando python-dotenv.
"""

import os
from config_azure_keyvault import cargar_secretos_keyvault
cargar_secretos_keyvault()

# Función para obtener credenciales de Jira

def get_jira_credentials():
    return {
        'user': os.getenv('JIRA_USER'),
        'token': os.getenv('JIRA_TOKEN'),
        'url': os.getenv('JIRA_URL')
    }

# Puedes agregar más funciones para otras integraciones aquí

# LLM (OpenAI, Azure, etc.)
def get_llm_credentials():
    return {
        'api_key': os.getenv('OPENAI_API_KEY')
    }

# TestRail
def get_testrail_credentials():
    return {
        'user': os.getenv('TESTRAIL_USER'),
        'token': os.getenv('TESTRAIL_TOKEN'),
        'url': os.getenv('TESTRAIL_URL')
    }
