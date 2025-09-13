"""
training_engine.py
Motor de entrenamiento especializado para proyectos de automatización QA.
Extrae patrones, estructuras y buenas prácticas del código base.
"""
import os
import re
import json
from pathlib import Path

class QATrainingEngine:
    def __init__(self, project_path):
        self.project_path = project_path
        self.patterns = {
            'page_objects': [],
            'test_methods': [],
            'step_definitions': [],
            'utilities': [],
            'test_data': []
        }
        self.project_type = 'unknown'  # 'mobile', 'web', 'hybrid'
        self.frameworks = []
        
    def analyze_project(self):
        """Analiza el proyecto de automatización para extraer patrones"""
        
        for root, dirs, files in os.walk(self.project_path):
            # Skip directorios innecesarios
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for file in files:
                if file.endswith(('.java', '.py', '.js', '.ts')):
                    file_path = os.path.join(root, file)
                    self._analyze_file(file_path)
    
    def _analyze_file(self, file_path):
        """Analiza archivo individual para extraer patrones"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                filename = os.path.basename(file_path)
                
                # Detectar Page Objects/Screens - Móvil
                if ('screen' in filename.lower() or 'activity' in filename.lower() or 
                    'page' in filename.lower() or 'Screen' in content or 'Activity' in content):
                    self._extract_page_object_patterns(content, filename)
                
                # Detectar métodos de test
                if 'test' in filename.lower() or '@Test' in content or 'def test_' in content:
                    self._extract_test_patterns(content, filename)
                
                # Detectar step definitions
                if 'step' in filename.lower() or '@Given' in content or '@When' in content:
                    self._extract_step_patterns(content, filename)
                
                # Detectar utilities/tasks
                if ('util' in filename.lower() or 'helper' in filename.lower() or 
                    'task' in filename.lower() or filename in ['Login.java', 'SearchCustomer.java', 
                    'AddOrder.java', 'Synchronization.java']):
                    self._extract_utility_patterns(content, filename)
                    
        except Exception as e:
            print(f"Error analizando {file_path}: {e}")
    
    def _extract_page_object_patterns(self, content, filename):
        """Extrae patrones de Page Objects específicos para automatización móvil"""
        
        # Buscar declaraciones de localizadores móviles
        mobile_locators = []
        
        # Pattern para By.id() con package específico de móvil
        by_locators = re.findall(r'By\.(id|name|xpath|className|accessibilityId)\s*\(\s*["\']([^"\']+)["\']\s*\)', content)
        mobile_locators.extend([loc[1] for loc in by_locators])
        
        # Pattern para strings de locators de Android (package:id/elemento)
        android_locators = re.findall(r'"([\w\.]+:id/\w+)"', content)
        mobile_locators.extend(android_locators)
        
        # Buscar controles móviles específicos
        mobile_controls = re.findall(r'(?:public|private)\s+(TextBox|Button|Label|CheckBox|ComboBox|AppiumControl)\s+(\w+)', content)
        
        # Buscar métodos de acción específicos para móvil
        mobile_actions = re.findall(
            r'(?:public|def)\s+(?:void\s+)?(\w*(?:click|setText|getText|tap|swipe|scroll|isDisplayed|isEnabled|clear|findControl)\w*)\s*\(', 
            content, re.IGNORECASE
        )
        
        # Buscar estructura de clase (Screen, Activity, Page)
        class_pattern = re.search(r'(?:public\s+)?class\s+(\w+(?:Screen|Activity|Page))', content)
        class_name = class_pattern.group(1) if class_pattern else filename.replace('.java', '')
        
        # Solo agregar si tiene elementos relevantes para móvil
        if mobile_locators or mobile_controls or ('Screen' in filename) or ('Activity' in filename):
            pattern = {
                'file': filename,
                'class_name': class_name,
                'locators': mobile_locators[:10],  # Limitar a 10 locators
                'mobile_controls': [{'type': ctrl[0], 'name': ctrl[1]} for ctrl in mobile_controls[:8]],
                'action_methods': mobile_actions[:10]
            }
            
            # Generar código de ejemplo específico para móvil
            if mobile_controls:
                sample_lines = []
                for ctrl in mobile_controls[:3]:
                    if android_locators:
                        sample_lines.append(f'public {ctrl[0]} {ctrl[1]} = new {ctrl[0]}(By.id("{android_locators[0]}"));')
                    else:
                        sample_lines.append(f'public {ctrl[0]} {ctrl[1]} = new {ctrl[0]}(By.id("locator"));')
                pattern['sample_code'] = '\n'.join(sample_lines)
            else:
                pattern['sample_code'] = content[:300]  # Muestra del código
            
            self.patterns['page_objects'].append(pattern)
    
    def _extract_test_patterns(self, content, filename):
        """Extrae patrones de métodos de test"""
        
        # Buscar métodos de test
        test_methods = re.findall(
            r'(?:@Test|def test_|it\()\s*["\']?([^"\'()]+)?["\']?\s*', 
            content, re.IGNORECASE
        )
        
        # Buscar assertions
        assertions = re.findall(
            r'(assert\w*|expect|should|verify)\s*\(', 
            content, re.IGNORECASE
        )
        
        # Buscar setup/teardown
        setup_patterns = re.findall(
            r'(?:@Before|@After|setUp|tearDown|beforeEach|afterEach)', 
            content, re.IGNORECASE
        )
        
        if test_methods or assertions:
            self.patterns['test_methods'].append({
                'file': filename,
                'test_methods': test_methods[:5],
                'assertions': list(set(assertions))[:5],
                'setup_teardown': setup_patterns,
                'sample_code': content[:500]
            })
    
    def _extract_step_patterns(self, content, filename):
        """Extrae patrones de Step Definitions con más detalles"""
        
        # Buscar steps de Cucumber con anotaciones completas
        cucumber_steps = []
        
        # Pattern mejorado para capturar Given/When/Then/And
        step_patterns = re.findall(
            r'@(Given|When|Then|And)\s*\(\s*["\']([^"\']+)["\']\s*\)\s*\n\s*public\s+void\s+(\w+)\s*\([^)]*\)', 
            content, re.MULTILINE
        )
        
        for step_type, step_text, method_name in step_patterns:
            cucumber_steps.append({
                'type': step_type,
                'text': step_text,
                'method': method_name
            })
        
        # Buscar steps básicos (solo texto)
        basic_steps = re.findall(
            r'@(?:Given|When|Then|And)\s*\(\s*["\']([^"\']+)["\']', 
            content
        )
        
        # Buscar imports para detectar frameworks
        imports = re.findall(r'import\s+([\w\.]+);', content)
        frameworks = []
        if any('cucumber' in imp.lower() for imp in imports):
            frameworks.append('Cucumber')
        if any('junit' in imp.lower() for imp in imports):
            frameworks.append('JUnit')
        if any('appium' in imp.lower() for imp in imports):
            frameworks.append('Appium')
        
        # Buscar instancias de tasks/screens
        task_instances = re.findall(r'(\w+)\s+(\w+)\s*=\s*new\s+(\w+)\s*\(\s*\)', content)
        
        if cucumber_steps or basic_steps:
            pattern = {
                'file': filename,
                'steps': basic_steps,
                'detailed_steps': cucumber_steps,
                'frameworks': frameworks,
                'task_instances': [{'type': task[0], 'name': task[1], 'class': task[2]} for task in task_instances[:5]]
            }
            
            # Generar código de ejemplo con contexto
            if step_patterns:
                sample_lines = []
                for step in step_patterns[:2]:  # Primeros 2 steps
                    sample_lines.append(f'@{step[0]}("{step[1]}")')
                    sample_lines.append(f'public void {step[2]}() {{')
                    sample_lines.append('    // Implementación aquí')
                    sample_lines.append('}')
                    sample_lines.append('')
                pattern['sample_code'] = '\n'.join(sample_lines)
            else:
                pattern['sample_code'] = content[:400]
            
            self.patterns['step_definitions'].append(pattern)
    
    def _extract_utility_patterns(self, content, filename):
        """Extrae patrones de utilities y tasks"""
        
        # Buscar métodos públicos
        utility_methods = re.findall(
            r'public\s+(?:static\s+)?(?:\w+\s+)?(\w+)\s*\([^}]*\)', 
            content
        )
        
        # Buscar imports para detectar tipo de utility
        imports = re.findall(r'import\s+([\w\.]+);', content)
        utility_type = 'utility'
        
        if any('appium' in imp.lower() for imp in imports):
            utility_type = 'mobile_utility'
        if any('selenium' in imp.lower() for imp in imports):
            utility_type = 'web_utility'
        if filename.endswith('Task.java') or filename in ['Login.java', 'AddOrder.java', 'SearchCustomer.java']:
            utility_type = 'task'
        
        # Buscar patrones específicos para tasks de negocio
        business_methods = re.findall(
            r'public\s+void\s+(with\w*|execute\w*|perform\w*|do\w*)\s*\([^}]*\)', 
            content
        )
        
        # Buscar uso de screens/activities
        screen_usage = re.findall(r'(\w+Screen)\s+(\w+)\s*=\s*new\s+\w+Screen\s*\(\s*\)', content)
        
        if utility_methods or business_methods:
            pattern = {
                'file': filename,
                'utility_type': utility_type,
                'utility_methods': utility_methods[:8],
                'business_methods': business_methods,
                'screen_usage': [{'screen': screen[0], 'instance': screen[1]} for screen in screen_usage]
            }
            
            # Generar código de ejemplo específico para tasks
            if utility_type == 'task' and business_methods:
                sample_lines = []
                sample_lines.append(f'public class {filename.replace(".java", "")} {{')
                if screen_usage:
                    sample_lines.append(f'    {screen_usage[0][0]} {screen_usage[0][1]} = new {screen_usage[0][0]}();')
                    sample_lines.append('')
                for method in business_methods[:2]:
                    sample_lines.append(f'    public void {method}() {{')
                    sample_lines.append('        // Lógica de negocio aquí')
                    sample_lines.append('    }')
                sample_lines.append('}')
                pattern['sample_code'] = '\n'.join(sample_lines)
            else:
                pattern['sample_code'] = content[:400]
            
            self.patterns['utilities'].append(pattern)
    
    def generate_training_prompt(self):
        """Genera prompt de entrenamiento basado en patrones extraídos"""
        
        training_prompt = """ENTRENAMIENTO ESPECIALIZADO - PROYECTO QA AUTOMATION

Tu misión es generar código de pruebas automáticas basándote EXCLUSIVAMENTE en los patrones y estructuras encontradas en este proyecto específico.

=== PATRONES DEL PROYECTO ===

"""
        
        # Page Objects detectados
        if self.patterns['page_objects']:
            training_prompt += "📄 PAGE OBJECTS DETECTADOS:\n"
            for po in self.patterns['page_objects'][:3]:  # Solo primeros 3
                training_prompt += f"- Clase: {po['class_name']}\n"
                training_prompt += f"  Métodos: {', '.join(po['action_methods'][:5])}\n"
                training_prompt += f"  Locators ejemplo: {po['locators'][:3]}\n\n"
        
        # Tests detectados
        if self.patterns['test_methods']:
            training_prompt += "🧪 ESTRUCTURA DE TESTS:\n"
            for test in self.patterns['test_methods'][:3]:
                training_prompt += f"- Archivo: {test['file']}\n"
                training_prompt += f"  Métodos test: {', '.join(test['test_methods'][:3])}\n"
                training_prompt += f"  Assertions: {', '.join(test['assertions'][:3])}\n\n"
        
        # Steps detectados
        if self.patterns['step_definitions']:
            training_prompt += "🥒 CUCUMBER STEPS:\n"
            for step in self.patterns['step_definitions'][:2]:
                training_prompt += f"- Steps: {', '.join(step['steps'][:3])}\n\n"
        
        # Utilities detectadas
        if self.patterns['utilities']:
            training_prompt += "🛠️ UTILIDADES:\n"
            for util in self.patterns['utilities'][:2]:
                training_prompt += f"- Métodos: {', '.join(util['utility_methods'][:5])}\n\n"
        
        training_prompt += """
=== INSTRUCCIONES DE GENERACIÓN ===

1. SIEMPRE usa los mismos nombres de clases, métodos y patrones encontrados arriba
2. MANTÉN la estructura y convenciones del proyecto
3. NO inventes nuevos patrones - usa solo los detectados
4. Cuando generes Page Objects, usa la misma estructura de locators
5. Cuando generes tests, usa los mismos tipos de assertions
6. CREA archivos siguiendo la estructura de carpetas del proyecto

RECUERDA: Eres un especialista en ESTE proyecto específico, no un experto genérico."""

        return training_prompt
    
    def save_training_data(self, output_file='training_data.json'):
        """Guarda datos de entrenamiento en JSON"""
        training_data = {
            'patterns': self.patterns,
            'training_prompt': self.generate_training_prompt(),
            'project_path': self.project_path
        }
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(training_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Datos de entrenamiento guardados en: {output_file}")
        except Exception as e:
            print(f"❌ Error guardando entrenamiento: {e}")
    
    def get_patterns_summary(self):
        """Retorna resumen de patrones encontrados"""
        return {
            'page_objects_found': len(self.patterns['page_objects']),
            'test_files_found': len(self.patterns['test_methods']),
            'step_definitions_found': len(self.patterns['step_definitions']),
            'utilities_found': len(self.patterns['utilities'])
        }

# Ejemplo de uso:
if __name__ == "__main__":
    # Analizar proyecto de automatización
    project_path = "ruta/a/tu/proyecto/automation"
    trainer = QATrainingEngine(project_path)
    trainer.analyze_project()
    
    # Generar entrenamiento
    training_prompt = trainer.generate_training_prompt()
    print(training_prompt)
    
    # Guardar datos
    trainer.save_training_data()
    
    # Ver resumen
    summary = trainer.get_patterns_summary()
    print(f"📊 Patrones encontrados: {summary}")
