"""
workspace_indexer.py
Indexa y analiza el workspace para detectar frameworks, clases y archivos relevantes.
"""
import os
import fnmatch

class WorkspaceIndexer:
    def __init__(self, root_path):
        self.root_path = root_path
        self.files = []
        self.frameworks = set()

    def index_workspace(self):
        for dirpath, _, filenames in os.walk(self.root_path):
            for filename in filenames:
                if fnmatch.fnmatch(filename, '*.java') or fnmatch.fnmatch(filename, '*.feature'):
                    self.files.append(os.path.join(dirpath, filename))
        self.detect_frameworks()

    def detect_frameworks(self):
        for file in self.files:
            if file.endswith('.feature'):
                self.frameworks.add('Cucumber')
            # Puedes agregar más detección aquí

    def get_index(self):
        return {
            'files': self.files,
            'frameworks': list(self.frameworks)
        }

# Uso:
# indexer = WorkspaceIndexer(root_path)
# indexer.index_workspace()
# index = indexer.get_index()
