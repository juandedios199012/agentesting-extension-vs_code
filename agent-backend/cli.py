
"""
cli.py
Punto de entrada OPTIMIZADO del backend. Inicialización rápida con lazy loading y cache.
"""
import sys
import os
from indexer.workspace_indexer import WorkspaceIndexer
from model.contextual_model import ContextualModel, safe_print
from generator.code_generator import CodeGenerator

# Cache global para reutilizar entre llamadas
_cached_model = None
_cached_index = None
_last_workspace_path = None

def get_cached_model(workspace_path):
    """Obtiene modelo cached o crea uno nuevo si es necesario"""
    global _cached_model, _cached_index, _last_workspace_path
    
    # Si el workspace cambió, invalidar cache
    if _last_workspace_path != workspace_path:
        _cached_model = None
        _cached_index = None
        _last_workspace_path = workspace_path
    
    # Si no hay cache, crear nuevo
    if _cached_model is None or _cached_index is None:
        indexer = WorkspaceIndexer(workspace_path)
        indexer.index_workspace()
        _cached_index = indexer.get_index()
        
        _cached_model = ContextualModel(_cached_index)
        _cached_model.train_on_workspace()
    
    return _cached_model, _cached_index

def main():
    # OPTIMIZACIÓN: Usar cache y inicialización lazy
    workspace_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    try:
        model, index = get_cached_model(workspace_path)
        
        # Recibe el prompt desde la extensión
        if len(sys.argv) > 1:
            prompt = sys.argv[1]
            
            # OPTIMIZACIÓN: Respuesta directa sin inicializar generator para prompts simples
            if prompt.lower().startswith('crear clase'):
                # Solo para creación de clases cargar el generator
                generator = CodeGenerator(index)
                class_name = prompt.split(' ', 2)[-1]
                framework = index['frameworks'][0] if index['frameworks'] else None
                code = generator.create_class(class_name, framework)
                safe_print(code)
            else:
                # Para otros prompts, respuesta directa
                response = model.generate_response(prompt)
                safe_print(response)
        else:
            safe_print("No se recibió prompt.")
            
    except Exception as e:
        safe_print(f"Error en el agente: {str(e)}")

if __name__ == "__main__":
    main()
