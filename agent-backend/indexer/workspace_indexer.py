"""
workspace_indexer.py
Indexa y analiza el workspace para detectar frameworks, clases y archivos relevantes.
OPTIMIZADO: Cache, filtros inteligentes y indexación incremental.
"""
import os
import fnmatch
import json
import hashlib
from pathlib import Path

class WorkspaceIndexer:
    def __init__(self, root_path):
        self.root_path = root_path
        self.files = []
        self.frameworks = set()
        self.cache_file = os.path.join(root_path, '.agentesting_cache.json')
        
    def _get_workspace_hash(self):
        """Genera hash del workspace para detectar cambios"""
        relevant_files = []
        try:
            for dirpath, _, filenames in os.walk(self.root_path):
                # Skip directorios innecesarios para velocidad
                if any(skip in dirpath for skip in ['.git', 'node_modules', '.vscode', '__pycache__', 'target', 'build']):
                    continue
                    
                for filename in filenames:
                    if any(filename.endswith(ext) for ext in ['.java', '.py', '.feature', '.js', '.ts', '.cs']):
                        file_path = os.path.join(dirpath, filename)
                        try:
                            stat = os.stat(file_path)
                            relevant_files.append(f"{file_path}:{stat.st_mtime}")
                        except:
                            continue
            
            workspace_signature = ''.join(sorted(relevant_files))
            return hashlib.md5(workspace_signature.encode()).hexdigest()
        except:
            return None

    def _load_cache(self):
        """Carga cache si existe y es válido"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                current_hash = self._get_workspace_hash()
                if cache_data.get('workspace_hash') == current_hash:
                    self.files = cache_data.get('files', [])
                    self.frameworks = set(cache_data.get('frameworks', []))
                    return True
        except:
            pass
        return False

    def _save_cache(self):
        """Guarda cache del workspace"""
        try:
            cache_data = {
                'workspace_hash': self._get_workspace_hash(),
                'files': self.files,
                'frameworks': list(self.frameworks)
            }
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2)
        except:
            pass

    def index_workspace(self):
        """Indexa workspace con cache inteligente"""
        # Intenta cargar desde cache
        if self._load_cache():
            return
        
        # Si no hay cache válido, indexa desde cero
        self.files = []
        self.frameworks = set()
        
        # Patrones de archivos relevantes para testing
        test_patterns = ['*.java', '*.py', '*.feature', '*.js', '*.ts', '*.cs', '*.rb']
        
        for dirpath, dirnames, filenames in os.walk(self.root_path):
            # Skip directorios innecesarios para mejorar velocidad
            dirnames[:] = [d for d in dirnames if not d.startswith('.') and d not in 
                          ['node_modules', '__pycache__', 'target', 'build', 'dist', 'bin']]
            
            for filename in filenames:
                if any(fnmatch.fnmatch(filename, pattern) for pattern in test_patterns):
                    full_path = os.path.join(dirpath, filename)
                    # Solo incluir archivos que probablemente sean de testing
                    if self._is_test_related(full_path, filename):
                        self.files.append(full_path)
        
        self.detect_frameworks()
        self._save_cache()

    def _is_test_related(self, file_path, filename):
        """Determina si un archivo es relevante para testing"""
        test_indicators = [
            'test', 'spec', 'feature', 'page', 'step', 
            'automation', 'selenium', 'webdriver', 'api'
        ]
        
        file_lower = filename.lower()
        path_lower = file_path.lower()
        
        # Archivos claramente de testing
        if any(indicator in file_lower or indicator in path_lower for indicator in test_indicators):
            return True
            
        # Archivos .feature siempre son relevantes
        if filename.endswith('.feature'):
            return True
            
        # Limitar a archivos en directorios de testing
        if any(test_dir in path_lower for test_dir in ['test', 'spec', 'e2e', 'integration']):
            return True
            
        return False

    def detect_frameworks(self):
        """Detecta frameworks de testing basado en archivos y contenido"""
        framework_indicators = {
            'Cucumber': ['.feature'],
            'Selenium': ['webdriver', 'selenium'],
            'Pytest': ['pytest', 'test_'],
            'JUnit': ['junit', '@Test'],
            'TestNG': ['testng', '@Test'],
            'Playwright': ['playwright'],
            'Cypress': ['cypress'],
            'Robot Framework': ['.robot'],
            'Jest': ['jest', '.spec.js', '.test.js'],
            'Mocha': ['mocha', 'describe('],
        }
        
        for file_path in self.files[:20]:  # Solo revisar primeros 20 archivos para velocidad
            try:
                filename = os.path.basename(file_path).lower()
                
                # Detectar por extensión/nombre
                for framework, indicators in framework_indicators.items():
                    if any(indicator in filename for indicator in indicators):
                        self.frameworks.add(framework)
                        continue
                
                # Para archivos Java/Python, revisar contenido brevemente
                if file_path.endswith(('.java', '.py')) and os.path.getsize(file_path) < 50000:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content_sample = f.read(2000)  # Solo primeros 2KB
                        content_lower = content_sample.lower()
                        
                        for framework, indicators in framework_indicators.items():
                            if any(indicator in content_lower for indicator in indicators):
                                self.frameworks.add(framework)
                                
            except:
                continue

    def get_index(self):
        return {
            'files': self.files[:50],  # Limitar archivos para mejor rendimiento
            'frameworks': list(self.frameworks),
            'total_files': len(self.files)
        }

# Uso:
# indexer = WorkspaceIndexer(root_path)
# indexer.index_workspace()
# index = indexer.get_index()
