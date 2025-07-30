
"""
cli.py
Punto de entrada del backend Copilot-like. Indexa workspace, entrena modelo contextual, responde a prompts y genera código/archivos.
"""
import sys
import os
from indexer.workspace_indexer import WorkspaceIndexer
from model.contextual_model import ContextualModel, safe_print
from generator.code_generator import CodeGenerator

def main():
    # Detecta el workspace automáticamente (directorio padre)
    workspace_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    indexer = WorkspaceIndexer(workspace_path)
    indexer.index_workspace()
    index = indexer.get_index()

    model = ContextualModel(index)
    model.train_on_workspace()

    generator = CodeGenerator(index)

    # Recibe el prompt desde la extensión
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        # Si el prompt pide crear una clase
        if prompt.lower().startswith('crear clase'):
            class_name = prompt.split(' ', 2)[-1]
            framework = index['frameworks'][0] if index['frameworks'] else None
            code = generator.create_class(class_name, framework)
            safe_print(code)
        else:
            response = model.generate_response(prompt)
            safe_print(response)
    else:
        safe_print("No se recibió prompt.")

if __name__ == "__main__":
    main()
