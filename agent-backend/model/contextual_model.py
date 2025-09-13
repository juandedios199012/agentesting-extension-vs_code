"""
contextual_model.py
Entrena y ajusta el modelo LLM usando LangChain y el código fuente indexado.
"""

import os
import sys
from langchain_openai import ChatOpenAI
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
            # OPTIMIZACIÓN: Configuración más rápida para GPT-3.5-turbo
            self.llm = ChatOpenAI(
                temperature=0.1,  # Menor temperatura = respuestas más rápidas y consistentes
                model_name="gpt-3.5-turbo", 
                openai_api_key=openai_api_key,
                max_tokens=500,  # Limitar tokens para respuestas más rápidas
                request_timeout=15  # Timeout de 15 segundos
            )
            safe_print("[SUCCESS] AgentestingMIA funcionando con IA completa")
        
        self.index = index
        self.frameworks = ', '.join(index.get('frameworks', []))
        self.model_path = model_path
        self.training_data = []
        self._load_training_data()
        
        # CACHE: Pre-construir contexto base para evitar recalcular
        self._base_context = self._build_base_context()
    
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
        OPTIMIZADO: Entrenamiento ligero y cache de contexto
        """
        if new_examples:
            self.training_data.extend(new_examples)
            self._save_training_data()
        # Entrenamiento ligero - solo actualizar context cache si hay cambios
        if not hasattr(self, '_base_context'):
            self._base_context = self._build_base_context()

    def _build_base_context(self):
        """Construye contexto base una sola vez para reutilizar"""
        # Intentar cargar entrenamiento especializado
        specialized_training = self._load_specialized_training()
        
        context_examples = '\n'.join([
            f"Prompt: {ex['prompt']}\nRespuesta: {ex['response']}" 
            for ex in self.training_data[-3:]  # Solo últimos 3 ejemplos
        ])
        
        base_context = f"""Eres AgentestingMIA, un agente experto en QA Automation especializado en generar código de pruebas.

PROYECTO ACTUAL:
- Frameworks detectados: {self.frameworks}
- Archivos analizados: {self.index.get('total_files', 0)}

{specialized_training}

CAPACIDADES:
1. Generar código de pruebas basado en patrones del proyecto
2. Crear archivos automáticamente cuando sea necesario
3. Sugerir mejores prácticas de QA

FORMATO PARA CREAR ARCHIVOS:
ARCHIVO: ruta/del/archivo.ext
CONTENIDO:
[código aquí]

CONTEXTO PREVIO:
{context_examples}

Responde de forma concisa y específica."""

        return base_context
    
    def _load_specialized_training(self):
        """Carga entrenamiento especializado del proyecto (móvil/web/híbrido)"""
        try:
            import json
            training_file = os.path.join(os.path.dirname(__file__), '..', 'training', 'training_data.json')
            web_patterns_file = os.path.join(os.path.dirname(__file__), '..', 'training', 'web_automation_patterns.json')
            
            specialized_context = ""
            
            # Cargar entrenamiento principal
            if os.path.exists(training_file):
                with open(training_file, 'r', encoding='utf-8') as f:
                    training_data = json.load(f)
                    
                specialized_context += training_data.get('training_prompt', '')
                project_type = training_data.get('project_type', 'mobile')
                frameworks = training_data.get('frameworks', [])
                
                # Información del proyecto
                specialized_context += f"\n\n=== INFORMACIÓN DEL PROYECTO ===\n"
                specialized_context += f"Tipo: {project_type}\n"
                specialized_context += f"Frameworks: {', '.join(frameworks)}\n"
                
                # Si tiene patrones web también
                if 'web_pages' in training_data and training_data['web_pages']:
                    specialized_context += "\n🌐 PROYECTO HÍBRIDO DETECTADO - Móvil + Web\n"
                    specialized_context += "Usa la misma arquitectura Task-Page/Screen-Control para ambos tipos.\n"
            
            # Cargar patrones web base si existen
            if os.path.exists(web_patterns_file):
                with open(web_patterns_file, 'r', encoding='utf-8') as f:
                    web_data = json.load(f)
                    web_prompt = web_data.get('web_training_prompt', '')
                    if web_prompt:
                        specialized_context += f"\n\n{web_prompt}"
            
            if specialized_context:
                return specialized_context
            else:
                return self._create_basic_training()
            
        except Exception as e:
            return "INSTRUCCIÓN: Genera código de automatización de pruebas siguiendo mejores prácticas."
    
    def _create_basic_training(self):
        """Crea entrenamiento básico basado en archivos detectados"""
        sample_files = self.index.get('files', [])[:5]  # Primeros 5 archivos
        
        training = """
=== ENTRENAMIENTO PROYECTO ESPECÍFICO ===

IMPORTANTE: Debes generar código que siga los patrones encontrados en este proyecto.

ARCHIVOS DETECTADOS:
"""
        
        for file_path in sample_files:
            try:
                filename = os.path.basename(file_path)
                if 'page' in filename.lower():
                    training += f"📄 Page Object: {filename}\n"
                elif 'test' in filename.lower():
                    training += f"🧪 Test: {filename}\n"
                elif 'step' in filename.lower():
                    training += f"🥒 Step Definition: {filename}\n"
                elif '.feature' in filename:
                    training += f"📝 Feature: {filename}\n"
            except:
                continue
        
        training += f"""
FRAMEWORKS DETECTADOS: {self.frameworks}

INSTRUCCIONES:
1. Usa SOLO los patrones de este proyecto
2. Mantén la estructura de carpetas detectada
3. No inventes nuevos frameworks - usa los detectados
4. Genera código consistente con el proyecto existente
"""
        
        return training

    def generate_response(self, prompt):
        # Si está en modo demo (sin API key), guía al usuario a configurar
        if self.demo_mode:
            return self._generate_setup_guidance(prompt)
        
        # OPTIMIZACIÓN: Respuestas rápidas para saludos sin llamar API
        if self._is_simple_greeting(prompt):
            return self._generate_friendly_greeting()
        
        # OPTIMIZACIÓN: Usar contexto pre-construido
        try:
            # Usar contexto base + prompt específico
            final_message = f"{self._base_context}\n\nSOLICITUD: {prompt}"
            
            messages = [HumanMessage(content=final_message)]
            response = self.llm.invoke(messages)
            
            # Guardar interacción para aprendizaje futuro
            self._save_interaction(prompt, response.content if hasattr(response, 'content') else str(response))
            
            if hasattr(response, 'content'):
                return response.content
            else:
                return str(response)
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"
    
    def _save_interaction(self, prompt, response):
        """Guarda interacciones para mejorar el contexto"""
        try:
            # Solo guardar interacciones útiles (no saludos)
            if not self._is_simple_greeting(prompt) and len(response) > 50:
                self.training_data.append({
                    'prompt': prompt[:100],  # Truncar para eficiencia
                    'response': response[:200]
                })
                # Mantener solo últimos 10 ejemplos
                if len(self.training_data) > 10:
                    self.training_data = self.training_data[-10:]
                self._save_training_data()
        except:
            pass
    
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
