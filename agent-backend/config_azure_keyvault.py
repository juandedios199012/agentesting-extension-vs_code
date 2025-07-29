"""
config_azure_keyvault.py
Carga secretos desde Azure Key Vault y los expone como variables de entorno.
"""
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Nombre del Key Vault (debe estar en variable de entorno AZURE_KEYVAULT_NAME)
KEYVAULT_NAME = os.getenv("AZURE_KEYVAULT_NAME", "agentesting")
KVUri = f"https://{KEYVAULT_NAME}.vault.azure.net"

# Inicializa el cliente de Azure Key Vault
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

# Mapeo de nombres de secretos en Key Vault a variables de entorno del agente

SECRET_NAMES = [
    "JIRA_USER",
    "JIRA_TOKEN",
    "JIRA_URL",
    "TESTRAIL_USER",
    "TESTRAIL_TOKEN",
    "TESTRAIL_URL",
    "OPENAI_API_KEY"
]

def cargar_secretos_keyvault():
    for secret_name in SECRET_NAMES:
        try:
            secret = client.get_secret(secret_name.replace('_', '-'))
            os.environ[secret_name] = secret.value
        except Exception as e:
            print(f"[KeyVault] No se pudo cargar el secreto {secret_name}: {e}")
    # Verificación automática de la variable OPENAI_API_KEY
    if not os.environ.get("OPENAI_API_KEY"):
        print("[KeyVault] ADVERTENCIA: La variable OPENAI_API_KEY no está disponible en el entorno. El modelo OpenAI no funcionará.")
