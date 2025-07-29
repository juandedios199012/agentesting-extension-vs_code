"""
code_generator.py
Genera clases, archivos y casos de prueba usando solo patrones del proyecto actual.
"""


from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
import re

class CodeGenerator:
    def __init__(self, index):
        self.index = index
        self.frameworks = index.get('frameworks', [])
        self.files = index.get('files', [])
        self.llm = OpenAI(temperature=0.2)

    def extract_patterns(self):
        # Analiza los archivos del proyecto y extrae patrones de clases, métodos y estructuras
        patterns = []
        for file_path in self.files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # Extrae definiciones de clases y métodos (ejemplo para Java/Python)
                class_matches = re.findall(r'class\s+(\w+)', content)
                method_matches = re.findall(r'def\s+(\w+)', content)
                patterns.append({'file': file_path, 'classes': class_matches, 'methods': method_matches})
            except Exception:
                continue
        return patterns

    def detect_main_framework(self):
        # Detecta el framework principal del proyecto
        if self.frameworks:
            return self.frameworks[0]
        # Heurística: buscar por archivos o dependencias
        for file in self.files:
            if 'pytest' in file or 'test_' in file:
                return 'Pytest'
            if 'robot' in file:
                return 'Robot Framework'
            if file.endswith('.feature'):
                return 'Cucumber'
            if 'junit' in file.lower():
                return 'JUnit'
            if 'testng' in file.lower():
                return 'TestNG'
        return 'Generic'

    def create_class(self, class_name, framework=None):
        # Si no se especifica framework, detecta automáticamente
        if not framework:
            framework = self.detect_main_framework()
        # Extrae patrones del proyecto
        patterns = self.extract_patterns()
        # Usa LangChain/LLM para generar la clase adaptada al contexto
        template = PromptTemplate(
            input_variables=["class_name", "framework", "patterns"],
            template="""
Eres un agente experto en automatización de pruebas. El proyecto usa el framework: {framework}.
Analiza los siguientes patrones detectados en el código fuente:
{patterns}
Genera una clase llamada {class_name} siguiendo la estructura y convenciones del proyecto.
"""
        )
        patterns_str = str(patterns)
        final_prompt = template.format(class_name=class_name, framework=framework, patterns=patterns_str)
        return self.llm(final_prompt)

# Uso:
# generator = CodeGenerator(index)
# code = generator.create_class('Login')
