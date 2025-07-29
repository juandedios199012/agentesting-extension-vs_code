# Agente Python para Automatización de Pruebas

Este proyecto implementa un agente en Python que genera artefactos de automatización (archivos feature y step definitions) a partir de historias de usuario.

## Estructura del proyecto
- `main.py`: Ejemplo de integración y prueba del agente
- `cli.py`: Interfaz de línea de comandos para procesar historias y generar artefactos
- `gestor_historias.py`: Gestión de historias y generación de archivos
- `generador_cucumber.py`: Generación de features y steps en formato Cucumber
- `logger.py`: Registro centralizado de eventos y errores
- `entrenador.py`: Análisis y entrenamiento del agente con proyectos base
- Otros módulos de soporte

## Instalación
1. Clona el repositorio y navega a la carpeta del agente.
2. Instala Python 3.8+.
3. Instala dependencias si las hubiera (por ahora solo librerías estándar).

## Manejo seguro de credenciales
Para gestionar credenciales y configuraciones sensibles, utiliza un archivo `.env` junto con la librería `python-dotenv`.

### Patrón recomendado: configuración sensible centralizada
Las credenciales y configuraciones privadas se gestionan de forma centralizada en el módulo `config_secreta.py`. Solo los módulos que requieren acceso a datos sensibles deben importar y usar funciones de este archivo.

#### Ejemplo de uso en una integración externa
```python
from config_secreta import get_jira_credentials

creds = get_jira_credentials()
usuario = creds['user']
token = creds['token']
url = creds['url']
```

Si agregas nuevas integraciones (por ejemplo, para otras APIs), crea una función en `config_secreta.py` que exponga las variables necesarias y úsala en el módulo correspondiente.

#### Ejemplo de uso en integración con LLM (OpenAI, Azure, etc.)
```python
from config_secreta import get_llm_credentials

creds = get_llm_credentials()
api_key = creds['api_key']
api_url = creds['api_url']
```

#### Ejemplo de uso en integración con TestRail
```python
from config_secreta import get_testrail_credentials

creds = get_testrail_credentials()
usuario = creds['user']
token = creds['token']
url = creds['url']
```

### Instalación de python-dotenv
```powershell
pip install python-dotenv
```

### Ejemplo de archivo `.env`
```
JIRA_USER=tu_usuario
JIRA_TOKEN=tu_token
JIRA_URL=https://tujira.com
TESTRAIL_USER=tu_usuario_testrail
TESTRAIL_TOKEN=tu_token_testrail
TESTRAIL_URL=https://tutestrail.com
LLM_API_KEY=tu_api_key_llm
LLM_API_URL=https://api.llm.com/v1/completions
```

### Uso en el código
Importa y carga las variables de entorno en tus módulos:
```python
from dotenv import load_dotenv
import os

load_dotenv()
JIRA_USER = os.getenv('JIRA_USER')
JIRA_TOKEN = os.getenv('JIRA_TOKEN')
JIRA_URL = os.getenv('JIRA_URL')
```

## Uso de la CLI
Ejecuta el agente desde la terminal:

```powershell
python cli.py --historias "ruta/a/historias" --salida "ruta/a/salida"
```

### Ejemplo: generación automática de escenarios y steps con LLM
Puedes invocar el agente para analizar historias de usuario y generar artefactos enriquecidos usando el modelo LLM:

```powershell
python cli.py --historias "ruta/a/historias" --salida "ruta/a/salida" --usar-llm
```
Esto analizará cada historia usando el modelo de lenguaje configurado y sugerirá escenarios y steps adicionales.
```

## Ejemplo de historia de usuario
Coloca archivos `.txt` con historias en la carpeta indicada. Ejemplo:

```
Como usuario quiero poder iniciar sesión para acceder a mi perfil y funcionalidades personalizadas.
```

## Ejemplo de archivo feature generado
```
Feature: HistoriaUsuario
  Scenario: HistoriaUsuario
    Como usuario quiero poder iniciar sesión para acceder a mi perfil y funcionalidades personalizadas.
    Given el sistema está en estado inicial
    When el usuario realiza la acción principal
    Then se valida el resultado esperado
```

## Plugins y extensiones
El agente soporta plugins para ampliar funcionalidades de forma sencilla. Los plugins se ubican en la carpeta `plugins/` y deben heredar de la clase `BasePlugin`.

### Ejemplo de plugin
```python
from plugins.base_plugin import BasePlugin

class MiPlugin(BasePlugin):
    def ejecutar(self, datos):
        # Procesa los datos y retorna un resultado
        return f"Procesado por MiPlugin: {datos}"
```

### Uso de plugins
El agente descubre y ejecuta automáticamente todos los plugins en la carpeta `plugins/` sobre los datos que le indiques.

## Logs
Todos los eventos y errores se registran en el archivo `agente.log`.

## Autor
Diplomado Software Testing Bolivia
