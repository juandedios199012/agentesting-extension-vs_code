"""
hybrid_trainer.py
Entrenador híbrido que detecta y entrena patrones móviles y web manteniendo arquitectura consistente.
"""
import os
import re
import json
from pathlib import Path
from training_engine import QATrainingEngine

class HybridTrainingEngine(QATrainingEngine):
    """Motor de entrenamiento que maneja tanto patrones móviles como web"""
    
    def __init__(self, project_path):
        super().__init__(project_path)
        self.web_patterns = {
            'web_pages': [],
            'web_tasks': [],
            'web_controls': []
        }
        
    def analyze_project(self):
        """Analiza proyecto detectando patrones móviles y web"""
        print("🔍 Analizando proyecto híbrido...")
        
        # Detectar tipo de proyecto
        self._detect_project_type()
        
        # Analizar archivos
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for file in files:
                if file.endswith(('.java', '.py', '.js', '.ts')):
                    file_path = os.path.join(root, file)
                    self._analyze_file_hybrid(file_path)
                    
        return self._merge_patterns()
    
    def _detect_project_type(self):
        """Detecta si es proyecto móvil, web o híbrido"""
        mobile_indicators = []
        web_indicators = []
        
        # Buscar indicadores en archivos
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                if file.endswith(('.java', '.py', '.js', '.ts', '.xml', '.json')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            # Indicadores móviles
                            if any(keyword in content.lower() for keyword in ['appium', 'android', 'ios', 'mobile', 'device', 'androiddriver']):
                                mobile_indicators.append(file_path)
                            
                            # Indicadores web
                            if any(keyword in content.lower() for keyword in ['selenium', 'webdriver', 'browser', 'chrome', 'firefox', 'chromedriver']):
                                web_indicators.append(file_path)
                                
                            # Detectar frameworks
                            if 'cucumber' in content.lower():
                                if 'Cucumber' not in self.frameworks:
                                    self.frameworks.append('Cucumber')
                            if 'junit' in content.lower():
                                if 'JUnit' not in self.frameworks:
                                    self.frameworks.append('JUnit')
                            if 'appium' in content.lower():
                                if 'Appium' not in self.frameworks:
                                    self.frameworks.append('Appium')
                            if 'selenium' in content.lower():
                                if 'Selenium' not in self.frameworks:
                                    self.frameworks.append('Selenium')
                                    
                    except:
                        continue
        
        # Determinar tipo de proyecto
        if mobile_indicators and web_indicators:
            self.project_type = 'hybrid'
        elif mobile_indicators:
            self.project_type = 'mobile'
        elif web_indicators:
            self.project_type = 'web'
        else:
            self.project_type = 'unknown'
            
        print(f"📱 Tipo de proyecto detectado: {self.project_type}")
        print(f"🛠️ Frameworks detectados: {self.frameworks}")
        
        if mobile_indicators:
            print(f"   📱 Archivos móviles: {len(mobile_indicators)}")
        if web_indicators:
            print(f"   🌐 Archivos web: {len(web_indicators)}")
    
    def _analyze_file_hybrid(self, file_path):
        """Analiza archivo detectando si es móvil o web"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                filename = os.path.basename(file_path)
                
                # Detectar si es web o móvil
                is_web = self._is_web_file(content, filename)
                is_mobile = self._is_mobile_file(content, filename)
                
                if is_web:
                    self._extract_web_patterns(content, filename)
                elif is_mobile:
                    self._extract_mobile_patterns(content, filename)
                
                # Analizar step definitions (comunes)
                if 'step' in filename.lower() or '@Given' in content or '@When' in content:
                    self._extract_step_patterns(content, filename)
                    
        except Exception as e:
            print(f"Error analizando {file_path}: {e}")
    
    def _is_web_file(self, content, filename):
        """Detecta si el archivo es de automatización web"""
        web_indicators = [
            'webdriver', 'selenium', 'browser', 'chrome', 'firefox',
            'page.java', 'webpage', 'webelement', 'by.id', 'by.xpath',
            'driver.get', 'driver.navigate'
        ]
        return any(indicator in content.lower() for indicator in web_indicators)
    
    def _is_mobile_file(self, content, filename):
        """Detecta si el archivo es de automatización móvil"""
        mobile_indicators = [
            'appium', 'android', 'ios', 'mobile', 'screen.java',
            'com.', ':id/', 'androiddriver', 'iosdriver',
            'appiumdriver', 'mobileelement'
        ]
        return any(indicator in content.lower() for indicator in mobile_indicators)
    
    def _extract_web_patterns(self, content, filename):
        """Extrae patrones específicos de web"""
        # Detectar Web Pages
        if 'page' in filename.lower() or 'Page' in content:
            self._extract_web_page_patterns(content, filename)
        
        # Detectar Web Tasks
        if ('task' in filename.lower() or filename in ['LoginTask.java', 'SearchTask.java'] or
            'withCredentials' in content or 'withSearchCriteria' in content):
            self._extract_web_task_patterns(content, filename)
    
    def _extract_mobile_patterns(self, content, filename):
        """Extrae patrones específicos de móvil (usar método existente)"""
        if ('screen' in filename.lower() or 'activity' in filename.lower() or 
            'page' in filename.lower() or 'Screen' in content or 'Activity' in content):
            self._extract_page_object_patterns(content, filename)
    
    def _extract_web_page_patterns(self, content, filename):
        """Extrae patrones de Web Pages"""
        # Buscar locators web
        web_locators = []
        
        # By.id, By.name, By.xpath, etc.
        by_locators = re.findall(r'By\.(id|name|xpath|css|className|tagName)\s*\(\s*["\']([^"\']+)["\']\s*\)', content)
        web_locators.extend([f"{loc[0]}={loc[1]}" for loc in by_locators])
        
        # Buscar controles web
        web_controls = re.findall(r'(?:public|private)\s+(WebTextBox|WebButton|WebDropdown|WebCheckBox|WebLabel)\s+(\w+)', content)
        
        # Buscar métodos de acción web
        web_actions = re.findall(
            r'(?:public|def)\s+(?:void\s+)?(\w*(?:sendKeys|click|select|navigate|scroll|hover|isDisplayed|isEnabled)\w*)\s*\(', 
            content, re.IGNORECASE
        )
        
        # Buscar clase
        class_pattern = re.search(r'(?:public\s+)?class\s+(\w+(?:Page|PageObject))', content)
        class_name = class_pattern.group(1) if class_pattern else filename.replace('.java', '')
        
        if web_locators or web_controls or web_actions:
            pattern = {
                'file': filename,
                'class_name': class_name,
                'locators': web_locators[:10],
                'web_controls': [{'type': ctrl[0], 'name': ctrl[1]} for ctrl in web_controls[:8]],
                'action_methods': web_actions[:10],
                'automation_type': 'web'
            }
            
            # Generar código de ejemplo web
            if web_controls:
                sample_lines = []
                for ctrl in web_controls[:3]:
                    if by_locators:
                        sample_lines.append(f'public {ctrl[0]} {ctrl[1]} = new {ctrl[0]}(By.{by_locators[0][0]}("{by_locators[0][1]}"));')
                    else:
                        sample_lines.append(f'public {ctrl[0]} {ctrl[1]} = new {ctrl[0]}(By.id("element"));')
                pattern['sample_code'] = '\\n'.join(sample_lines)
            else:
                pattern['sample_code'] = content[:300]
            
            self.web_patterns['web_pages'].append(pattern)
    
    def _extract_web_task_patterns(self, content, filename):
        """Extrae patrones de Web Tasks"""
        # Buscar métodos de negocio web
        business_methods = re.findall(
            r'public\s+void\s+(with\w*|navigate\w*|perform\w*|execute\w*)\s*\([^}]*\)', 
            content
        )
        
        # Buscar uso de pages
        page_usage = re.findall(r'(\w+Page)\s+(\w+)\s*=\s*new\s+\w+Page\s*\(\s*\)', content)
        
        if business_methods or page_usage:
            pattern = {
                'file': filename,
                'utility_type': 'web_task',
                'business_methods': business_methods,
                'page_usage': [{'page': page[0], 'instance': page[1]} for page in page_usage],
                'automation_type': 'web'
            }
            
            # Generar código de ejemplo web task
            if page_usage:
                sample_lines = []
                sample_lines.append(f'public class {filename.replace(".java", "")} {{')
                sample_lines.append(f'    {page_usage[0][0]} {page_usage[0][1]} = new {page_usage[0][0]}();')
                sample_lines.append('')
                for method in business_methods[:2]:
                    sample_lines.append(f'    public void {method}() {{')
                    sample_lines.append('        // Lógica de negocio web aquí')
                    sample_lines.append('    }')
                sample_lines.append('}')
                pattern['sample_code'] = '\\n'.join(sample_lines)
            else:
                pattern['sample_code'] = content[:400]
                
            self.web_patterns['web_tasks'].append(pattern)
    
    def _merge_patterns(self):
        """Combina patrones móviles y web en un entrenamiento híbrido"""
        # Cargar patrones web existentes
        web_patterns_file = os.path.join(os.path.dirname(__file__), 'web_automation_patterns.json')
        web_base_patterns = {}
        
        if os.path.exists(web_patterns_file):
            with open(web_patterns_file, 'r', encoding='utf-8') as f:
                web_base_patterns = json.load(f)
        
        # Combinar patrones
        hybrid_patterns = {
            **self.patterns,  # Patrones móviles detectados
            'web_pages': self.web_patterns['web_pages'],
            'web_tasks': self.web_patterns['web_tasks'],
            'web_controls': web_base_patterns.get('web_automation_patterns', {}).get('web_controls', []),
            'project_type': self.project_type,
            'frameworks': self.frameworks,
            'consistency_rules': web_base_patterns.get('consistency_rules', {})
        }
        
        return hybrid_patterns
    
    def generate_hybrid_training_prompt(self, patterns):
        """Genera prompt híbrido para móvil y web"""
        mobile_prompt = super().generate_training_prompt()
        
        web_prompt = f"""
=== PATRONES WEB DETECTADOS ===

📄 WEB PAGES:
{self._format_web_pages(patterns.get('web_pages', []))}

🎯 WEB TASKS:
{self._format_web_tasks(patterns.get('web_tasks', []))}

=== ARQUITECTURA HÍBRIDA ===

🔄 CONVERSIÓN AUTOMÁTICA:
Móvil → Web
- Screen → Page
- TextBox → WebTextBox  
- Button → WebButton
- Appium locators → Selenium locators

📱 MÓVIL: Task-Screen-Control (Appium)
🌐 WEB: Task-Page-Control (Selenium)

=== REGLAS DE CONSISTENCIA ===

1. ✅ MANTÉN la misma arquitectura en ambos tipos
2. ✅ USA los mismos nombres de métodos de negocio
3. ✅ CONVIERTE automáticamente entre móvil y web cuando sea necesario
4. ✅ MANTÉN el estilo español para Cucumber steps
5. ✅ USA patterns específicos detectados en el proyecto
"""
        
        return mobile_prompt + web_prompt
    
    def _format_web_pages(self, web_pages):
        """Formatea web pages para el prompt"""
        if not web_pages:
            return "No se detectaron páginas web específicas."
        
        formatted = ""
        for page in web_pages[:3]:  # Primeras 3
            formatted += f"- Clase: {page['class_name']}\\n"
            formatted += f"  Locators: {page['locators'][:3]}\\n"
            formatted += f"  Controles: {[ctrl['type'] for ctrl in page['web_controls'][:3]]}\\n\\n"
        
        return formatted
    
    def _format_web_tasks(self, web_tasks):
        """Formatea web tasks para el prompt"""
        if not web_tasks:
            return "No se detectaron tasks web específicos."
        
        formatted = ""
        for task in web_tasks[:3]:  # Primeros 3
            formatted += f"- Task: {task['file']}\\n"
            formatted += f"  Métodos: {task['business_methods'][:3]}\\n"
            formatted += f"  Pages: {[usage['page'] for usage in task['page_usage'][:2]]}\\n\\n"
        
        return formatted

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("🤖 ENTRENADOR HÍBRIDO - MÓVIL & WEB")
        print()
        print("Uso:")
        print("    python hybrid_trainer.py <ruta_proyecto> [ruta_salida]")
        print()
        print("Ejemplos:")
        print("    python hybrid_trainer.py \"C:/mi-proyecto-automation\"")
        print("    python hybrid_trainer.py \"/home/user/selenium-project\" \"./custom_training.json\"")
        print()
        print("El entrenador analizará:")
        print("• 📱 Patrones móviles (Appium)")
        print("• 🌐 Patrones web (Selenium)")
        print("• 🥒 Step Definitions (Cucumber)")
        print("• 🔧 Tasks y utilities")
        print()
        print("Generará entrenamiento híbrido manteniendo arquitectura consistente.")
        sys.exit(1)
    
    project_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(project_path):
        print(f"❌ Error: El directorio {project_path} no existe")
        sys.exit(1)
    
    print("🤖 Iniciando entrenamiento híbrido...")
    print(f"📁 Proyecto: {project_path}")
    
    # Crear motor híbrido
    engine = HybridTrainingEngine(project_path)
    
    # Analizar proyecto
    patterns = engine.analyze_project()
    
    # Contar patrones
    mobile_pages = len(patterns.get('page_objects', []))
    web_pages = len(patterns.get('web_pages', []))
    mobile_tasks = len([u for u in patterns.get('utilities', []) if u.get('utility_type') == 'task'])
    web_tasks = len(patterns.get('web_tasks', []))
    step_defs = len(patterns.get('step_definitions', []))
    
    print(f"\\n📊 ANÁLISIS COMPLETADO:")
    print(f"   • 📱 Mobile Screens: {mobile_pages}")
    print(f"   • 🌐 Web Pages: {web_pages}")
    print(f"   • 📱 Mobile Tasks: {mobile_tasks}")
    print(f"   • 🌐 Web Tasks: {web_tasks}")
    print(f"   • 🥒 Step definitions: {step_defs}")
    print(f"   • 🛠️ Tipo: {patterns.get('project_type', 'unknown')}")
    print(f"   • 🔧 Frameworks: {patterns.get('frameworks', [])}")
    
    # Generar prompt híbrido
    training_prompt = engine.generate_hybrid_training_prompt(patterns)
    patterns['training_prompt'] = training_prompt
    patterns['project_path'] = project_path
    
    # Guardar
    if output_path:
        save_path = output_path
    else:
        save_path = os.path.join(os.path.dirname(__file__), 'training_data.json')
    
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(patterns, f, indent=2, ensure_ascii=False)
    
    print(f"\\n✅ Datos de entrenamiento híbrido guardados en: {os.path.abspath(save_path)}")
    print("✅ ENTRENAMIENTO HÍBRIDO COMPLETADO")
    print()
    print("El agente ahora conoce patrones de:")
    print("- 📱 Automatización móvil (Appium)")
    print("- 🌐 Automatización web (Selenium)")
    print("- 🔄 Conversión automática entre patrones")
    print("- 🏗️ Arquitectura consistente Task-Page/Screen-Control")
    print()
    print("🚀 El agente está listo para generar código móvil Y web!")
