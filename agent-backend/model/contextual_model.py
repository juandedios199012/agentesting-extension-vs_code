"""
contextual_model.py
Entrena y ajusta el modelo LLM usando LangChain y el código fuente indexado.
"""

import os
import sys
from langchain_openai import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
import pickle


def safe_print(message):
    """Print seguro que evita errores de codificación en Windows"""
    try:
        print(message)
    except UnicodeEncodeError:
        # Si hay error de codificación, usa ASCII
        print(message.encode('ascii', 'replace').decode('ascii'))


class ContextualModel:
    def __init__(self, index, model_path='context_model.pkl'):
        # Intenta obtener la API key de diferentes fuentes
        openai_api_key = self._get_api_key()
        
        if not openai_api_key:
            # Sin API key, funciona en modo limitado
            self.demo_mode = True
            self.llm = None
            safe_print("[WARNING] AgentestingMIA funcionando en modo limitado - Configure su API key de OpenAI para funcionalidad completa")
        else:
            self.demo_mode = False
            self.llm = ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)
            safe_print("[SUCCESS] AgentestingMIA funcionando con IA completa")
        
        self.index = index
        self.frameworks = ', '.join(index.get('frameworks', []))
        self.model_path = model_path
        self.training_data = []
        self._load_training_data()
    
    def _get_api_key(self):
        """Intenta obtener la API key de diferentes fuentes"""
        # 1. Variable de entorno
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            return api_key
        
        # 2. Argumento pasado desde la extensión
        if len(sys.argv) > 2:
            return sys.argv[2]
        
        # 3. Archivo de configuración local (si existe)
        config_file = os.path.join(os.path.dirname(__file__), '..', 'config.txt')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return f.read().strip()
        
        return None

    def _load_training_data(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                self.training_data = pickle.load(f)

    def _save_training_data(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.training_data, f)

    def train_on_workspace(self, new_examples=None):
        """
        Permite entrenar el agente con nuevos ejemplos/contexto del workspace.
        El usuario puede agregar ejemplos de prompts y respuestas para mejorar el modelo.
        """
        if new_examples:
            self.training_data.extend(new_examples)
            self._save_training_data()
        # Aquí podrías usar algoritmos ML/AI para ajustar el contexto, embeddings, etc.
        # Por ahora, se almacena el historial para enriquecer el contexto de los prompts.

    def generate_response(self, prompt):
        # Si está en modo demo (sin API key), guía al usuario a configurar
        if self.demo_mode:
            return self._generate_setup_guidance(prompt)
        
        # Detecta saludos simples para respuestas más amigables
        if self._is_simple_greeting(prompt):
            return self._generate_friendly_greeting()
        
        # Usa LangChain y el historial de entrenamiento para generar una respuesta contextual
        context_examples = '\n'.join([
            f"Prompt: {ex['prompt']}\nRespuesta: {ex['response']}" for ex in self.training_data[-5:]
        ])
        
        # Construye el mensaje del sistema con instrucciones para crear archivos
        system_message = f"""Eres un agente experto en QA Automation que puede crear archivos automáticamente. 
        
El proyecto usa los siguientes frameworks: {self.frameworks}.

INSTRUCCIONES IMPORTANTES:
1. Cuando generes código completo (clases, funciones, tests), SIEMPRE crea el archivo automáticamente
2. Usa el formato EXACTO: ARCHIVO: ruta/del/archivo.ext\\nCONTENIDO:\\n[código aquí]
3. Sugiere rutas apropiadas basadas en el tipo de código:
   - Tests: tests/ o test/
   - Clases principales: src/ o lib/
   - Configuración: config/ o .
   - Page Objects (Selenium): pages/ o page_objects/
   - Utilities: utils/ o helpers/

EJEMPLOS DE CUÁNDO CREAR ARCHIVOS:
- "Crea una clase LoginPage" → Crear archivo
- "Crea tests de login" → Crear archivo
- "Genera un test de API" → Crear archivo
- "Explica cómo hacer X" → NO crear archivo (solo explicar)

Ejemplos previos de entrenamiento:
{context_examples}

Responde el siguiente prompt de forma contextual y específica al proyecto."""

        # Usa el formato de mensajes correcto para ChatOpenAI
        try:
            messages = [
                HumanMessage(content=f"{system_message}\n\nPrompt: {prompt}")
            ]
            response = self.llm.invoke(messages)
            # Si la respuesta es un objeto, extrae el contenido
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    def _generate_setup_guidance(self, prompt):
        """Guía al usuario para configurar su API key de OpenAI"""
        return f"""**¡Configura tu API key para desbloquear el poder completo de AgentestingMIA!**

**Tu solicitud:** "{prompt}"

**Para obtener respuestas personalizadas con IA:**

**Paso 1: Obtén tu API key de OpenAI**
1. Ve a https://platform.openai.com/api-keys
2. Crea una cuenta o inicia sesión
3. Haz clic en "Create new secret key"
4. Copia la clave generada

**Paso 2: Configúrala como variable de entorno (RECOMENDADO)**
1. Win+R -> escribe: sysdm.cpl
2. Pestaña "Opciones avanzadas" -> "Variables de entorno"
3. Agregar nueva variable:
   - Nombre: OPENAI_API_KEY
   - Valor: tu-api-key-aquí
4. Reinicia VS Code

**Alternativa: Configurar en VS Code**
1. Ve a: `Archivo > Preferencias > Configuración`
2. Busca "AgentestingMIA"
3. Pega tu API key en el campo "Openai Api Key"
4. ¡Listo! Reinicia el comando para obtener respuestas de IA

**Costo aproximado:** ~$0.002 por consulta (muy económico)

**Lo que obtendrás con tu API key configurada:**
- Respuestas personalizadas con GPT-3.5
- Análisis específico de tu proyecto
- Código de pruebas generado automáticamente
- Sugerencias contextuales basadas en tu código
- Integración completa con frameworks modernos

**Ejemplo de lo que podrás generar:**
```python
# Con tu API key, esto se convertirá en código específico
# personalizado para tu proyecto y frameworks
class TestPersonalizado:
    # Código generado por IA basado en tu prompt exacto
    pass
```

**¿Problemas con la configuración?** 
Asegúrate de que tu API key comience con "sk-" y tenga suficiente crédito en tu cuenta OpenAI.

¡Una vez configurada, vuelve a enviar tu prompt y obtendrás respuestas completamente personalizadas!"""

    def _is_simple_greeting(self, prompt):
        """Detecta si el prompt es un saludo simple"""
        greetings = ['hola', 'hello', 'hi', 'buenas', 'buenos días', 'buenas tardes', 'buenas noches', 'hey', 'saludos']
        return prompt.lower().strip() in greetings
    
    def _generate_friendly_greeting(self):
        """Genera un saludo amigable específico para QA"""
        return """¡Hola! 👋 Soy **AgentestingMIA**, tu agente de IA especializado en **QA Automation**.

🤖 **¿En qué puedo ayudarte hoy?**

**Mis superpoderes incluyen:**
🧪 **Generar código de pruebas** automáticas personalizadas
📁 **Crear archivos automáticamente** (como GitHub Copilot)
🔍 **Analizar tu proyecto** y detectar frameworks
🚀 **Trabajar con frameworks modernos:** Selenium, Pytest, Playwright, Cypress, TestNG, etc.

**Ejemplos de lo que puedes pedirme:**
```
✨ "Crea una clase Page Object para login con Selenium"
✨ "Genera tests de API REST para el endpoint /users"  
✨ "Crea pruebas automatizadas para un formulario de registro"
✨ "Genera suite de pruebas para carrito de compras"
✨ "Crea validaciones para una tabla de datos"
```

**Solo describe lo que necesitas** y yo analizo automáticamente si debo:
- 📝 Generar código y crear archivos
- 💡 Explicar conceptos  
- 🛠️ Sugerir mejores prácticas

¡Estoy listo para automatizar tus pruebas! 🚀"""


# Uso:
# model = ContextualModel(index)
# model.train_on_workspace([{'prompt': '...', 'response': '...'}])
# response = model.generate_response(prompt)
