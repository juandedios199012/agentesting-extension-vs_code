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
    import sys
    try:
        if hasattr(sys.stdout, 'buffer'):
            sys.stdout.buffer.write((str(message) + '\n').encode('utf-8', 'replace'))
        else:
            print(str(message))
    except Exception:
        print(str(message).encode('utf-8', 'replace').decode('utf-8', 'replace'))


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
                model_name="gpt-4-turbo", 
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

        # CACHE LOCAL DE RESPUESTAS
        self._response_cache = {}
    
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
        
        base_context = f"""Eres AgentestingMIA, un agente experto en QA Automation especializado en generar código de pruebas automáticas.

🤖 COMPORTAMIENTO CLAVE: Cuando el usuario pide automatización, SIEMPRE debes:
1. PRIMERO sugerir las clases específicas basadas en tu entrenamiento
2. LUEGO preguntar si debe crearlas automáticamente
3. SER PROACTIVO y específico, no genérico

PROYECTO ACTUAL:
- Frameworks detectados: {self.frameworks}
- Archivos analizados: {self.index.get('total_files', 0)}

{specialized_training}

INSTRUCCIONES CRÍTICAS:
- Cuando pidan automatización para "carrito de compra", "login", etc. DEBES sugerir clases ESPECÍFICAS del entrenamiento
- NUNCA des respuestas genéricas como "usa Appium" - sé específico con código real
- SIEMPRE ofrece crear archivos automáticamente si el usuario confirma
- Usa EXACTAMENTE los patrones del training_data.json

FORMATO PARA CREAR ARCHIVOS:
ARCHIVO: ruta/del/archivo.ext
CONTENIDO:
[código aquí]

EJEMPLO DE RESPUESTA CORRECTA:
"Para automatización de carrito con login, necesitarás estas clases específicas:

📱 Page Objects:
- LoginScreen.java (login móvil)
- ProductScreen.java (productos)
- OrderScreen.java (carrito)
- PurchaseSummaryScreen.java (resumen compra)

📋 Tasks:
- Login.java (autenticación)
- AddOrder.java (agregar productos)
- SearchCustomer.java (buscar cliente)

🧪 Steps:
- LoginStepDefinition.java
- OrderCreateStepDefinition.java

¿Quieres que cree estas clases automáticamente con el código específico?"

CONTEXTO PREVIO:
{context_examples}

SIEMPRE sé específico y proactivo, no genérico."""

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

        # Detectar confirmación para crear archivos
        confirm_words = ['sí', 'si', 'procede', 'hazlo', 'crear', 'crea', 'ok', 'dale']
        if prompt.strip().lower() in confirm_words:
            # Aquí deberías tener la lógica para crear los archivos sugeridos
            # Simulación: crear archivos sugeridos en el último prompt
            # En producción, deberías guardar el último prompt de sugerencia
            created_files = self._create_suggested_files()
            return f"✅ Archivos creados automáticamente:\n{created_files}"

        try:
            # Caching local: si el prompt ya fue respondido, devolver respuesta cacheada
            cache_key = prompt.strip().lower()
            if cache_key in self._response_cache:
                return self._response_cache[cache_key]

            # Si es automatización, agrega contexto especializado
            if self._is_automation_request(prompt):
                final_message = f"{self._base_context}\n\nSOLICITUD: {prompt}"
            else:
                # Para cualquier frase, solo envía el prompt al modelo
                final_message = prompt

            messages = [HumanMessage(content=final_message)]
            response = self.llm.invoke(messages)

            # Guardar interacción para aprendizaje futuro
            self._save_interaction(prompt, response.content if hasattr(response, 'content') else str(response))

            if hasattr(response, 'content'):
                result = response.content
            else:
                result = str(response)

            # Guardar en cache local
            self._response_cache[cache_key] = result
            return result
        except Exception as e:
            return f"Error al generar respuesta: {str(e)}"

    def _create_suggested_files(self):
        # Extraer nombres y contenido de clases de la última respuesta generada
        # Buscar en el cache local la última respuesta relevante
        import re
        files = []
        # Buscar la última respuesta que contenga 'ARCHIVO:' o bloques de código java
        for key in reversed(list(self._response_cache.keys())):
            response = self._response_cache[key]
            # Extraer archivos con formato ARCHIVO:
            matches = re.findall(r'ARCHIVO: ([^\n]+)\n```java\n([\s\S]+?)```', response)
            for file_path, code in matches:
                files.append((file_path.strip(), code.strip()))
            # Si no hay formato ARCHIVO, buscar bloques de código java y asignar nombres genéricos
            if not files:
                code_blocks = re.findall(r'```java\n([\s\S]+?)```', response)
                # Nombres sugeridos por el usuario
                suggested_names = [
                    'CustomerInformationScreen.java',
                    'ManageCustomerTask.java',
                    'CustomerManagementStepDefinition.java'
                ]
                for i, code in enumerate(code_blocks):
                    name = suggested_names[i] if i < len(suggested_names) else f'GeneratedClass{i+1}.java'
                    files.append((f'src/test/{name}', code.strip()))
            if files:
                break
        # Si no se encontró nada, fallback a ejemplo
        if not files:
            files = [
                ('src/test/CustomerInformationScreen.java', 'public class CustomerInformationScreen {}'),
                ('src/test/ManageCustomerTask.java', 'public class ManageCustomerTask {}'),
                ('src/test/CustomerManagementStepDefinition.java', 'public class CustomerManagementStepDefinition {}'),
            ]
        created = []
        for path, content in files:
            try:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                created.append(f"{path}")
            except Exception as e:
                created.append(f"{path} (error: {e})")
        return '\n'.join(created)
    
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
    
    def _is_automation_request(self, prompt):
        """Detecta si el usuario está pidiendo automatización específica"""
        automation_keywords = [
            'automatizar', 'automatización', 'crear proyecto', 'crea', 'generar',
            'carrito', 'login', 'página', 'formulario', 'página de', 'app',
            'móvil', 'mobile', 'proyecto de', 'suite de pruebas', 'test',
            'pruebas para', 'automatizar pruebas'
        ]
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in automation_keywords)
    
    def _generate_specific_automation_response(self, prompt):
        """Genera respuesta específica basada en el entrenamiento móvil"""
        try:
            # Cargar training data para respuestas específicas
            import json
            training_file = os.path.join(os.path.dirname(__file__), '..', 'training', 'training_data.json')
            
            if os.path.exists(training_file):
                with open(training_file, 'r', encoding='utf-8') as f:
                    training_data = json.load(f)
                    
                    # Extraer clases específicas del entrenamiento
                    page_objects = training_data.get('patterns', {}).get('page_objects', [])
                    step_definitions = training_data.get('patterns', {}).get('step_definitions', [])
                    utilities = training_data.get('patterns', {}).get('utilities', [])
                    
                    # Generar respuesta específica para carrito/login
                    response = f"""🎯 **Para automatización {self._extract_scenario(prompt)}, necesitarás estas clases específicas basadas en tu entrenamiento móvil:**

📱 **Page Objects (Screens):**"""
                    
                    # Filtrar Page Objects relevantes
                    relevant_pages = []
                    prompt_lower = prompt.lower()
                    
                    for page in page_objects:
                        class_name = page.get('class_name', '')
                        if ('login' in prompt_lower and 'Login' in class_name) or \
                           ('carrito' in prompt_lower or 'order' in prompt_lower and 'Order' in class_name) or \
                           ('product' in prompt_lower and 'Product' in class_name) or \
                           ('customer' in prompt_lower and 'Customer' in class_name):
                            relevant_pages.append(page)
                    
                    # Si no hay específicos, tomar los principales
                    if not relevant_pages:
                        relevant_pages = page_objects[:4]  # Tomar los primeros 4
                    
                    for page in relevant_pages[:5]:  # Máximo 5
                        class_name = page.get('class_name', 'Screen')
                        sample_controls = page.get('mobile_controls', [])[:3]  # 3 controles ejemplo
                        
                        response += f"\n- **{class_name}** - Controles: "
                        if sample_controls:
                            controls_str = ', '.join([f"{c.get('name', '')} ({c.get('type', '')})" for c in sample_controls])
                            response += controls_str
                        else:
                            response += "pantalla móvil"
                    
                    response += f"\n\n📋 **Tasks (Lógica de negocio):**"
                    for utility in utilities[:4]:  # Máximo 4 tasks
                        if utility.get('utility_type') == 'task':
                            file_name = utility.get('file', 'Task')
                            methods = utility.get('utility_methods', [])[:2]  # 2 métodos ejemplo
                            response += f"\n- **{file_name}** - Métodos: {', '.join(methods) if methods else 'lógica de negocio'}"
                    
                    response += f"\n\n🧪 **Step Definitions (Cucumber):**"
                    for step in step_definitions[:3]:  # Máximo 3 step definitions
                        file_name = step.get('file', 'StepDefinition')
                        sample_steps = step.get('steps', [])[:2]  # 2 steps ejemplo
                        response += f"\n- **{file_name}**"
                        if sample_steps:
                            response += f" - Steps: {', '.join(sample_steps)}"
                    
                    response += f"""\n\n🔧 **Arquitectura del proyecto:**
- **Frameworks:** Appium + Cucumber + JUnit
- **Patrón:** Task-Screen-Control (móvil)
- **Locators:** Android com.uniflex.flexbusinessandroid:id/...
- **Assertions:** assertTrue, assertEquals

💡 **¿Quieres que cree estas clases automáticamente con código específico?**

Solo responde "sí" o especifica qué clases necesitas primero, y generaré el código completo usando los patrones exactos de tu entrenamiento móvil."""
                    
                    return response
            
        except Exception as e:
            pass
        
        # Fallback: respuesta genérica si falla
        return """Para automatización móvil, te recomiendo crear:

📱 **Page Objects:** LoginScreen, ProductScreen, OrderScreen  
📋 **Tasks:** Login, AddOrder, SearchCustomer  
🧪 **Steps:** LoginStepDefinition, OrderCreateStepDefinition  

¿Quieres que genere el código específico?"""
    
    def _extract_scenario(self, prompt):
        """Extrae el escenario específico del prompt"""
        prompt_lower = prompt.lower()
        if 'carrito' in prompt_lower or 'compra' in prompt_lower:
            return "de carrito de compras"
        elif 'login' in prompt_lower:
            return "de login"
        elif 'formulario' in prompt_lower:
            return "de formulario"
        elif 'móvil' in prompt_lower or 'mobile' in prompt_lower:
            return "móvil"
        else:
            return "de aplicación"
    
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
