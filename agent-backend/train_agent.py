"""
train_agent.py
Script para entrenar AgentestingMIA con un proyecto específico de automatización.
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from training.training_engine import QATrainingEngine

def train_with_project(project_path, output_path=None):
    """Entrena el agente con un proyecto específico"""
    
    if not os.path.exists(project_path):
        print(f"❌ Error: La ruta {project_path} no existe")
        return False
    
    print(f"🤖 Iniciando entrenamiento de AgentestingMIA...")
    print(f"📁 Proyecto: {project_path}")
    
    # Crear motor de entrenamiento
    trainer = QATrainingEngine(project_path)
    
    # Analizar proyecto
    print("🔍 Analizando proyecto...")
    trainer.analyze_project()
    
    # Obtener resumen
    summary = trainer.get_patterns_summary()
    print(f"""
📊 ANÁLISIS COMPLETADO:
   • Page Objects encontrados: {summary['page_objects_found']}
   • Archivos de test: {summary['test_files_found']} 
   • Step definitions: {summary['step_definitions_found']}
   • Utilities: {summary['utilities_found']}
""")
    
    # Generar entrenamiento
    training_prompt = trainer.generate_training_prompt()
    print("🧠 Generando datos de entrenamiento...")
    
    # Guardar datos
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), 'training', 'training_data.json')
    
    # Asegurar que el directorio existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    trainer.save_training_data(output_path)
    
    print(f"""
✅ ENTRENAMIENTO COMPLETADO

El agente ahora conoce los patrones de tu proyecto:
- Estructura de clases detectada
- Convenciones de naming identificadas  
- Frameworks y herramientas reconocidos
- Mejores prácticas del proyecto aprendidas

🚀 El agente está listo para generar código específico para tu proyecto!

Archivo de entrenamiento: {output_path}
""")
    
    return True

def show_usage():
    """Muestra instrucciones de uso"""
    print("""
🤖 ENTRENADOR DE AGENTESTINGMIA

Uso:
    python train_agent.py <ruta_proyecto> [ruta_salida]

Ejemplos:
    python train_agent.py "C:/mi-proyecto-automation"
    python train_agent.py "/home/user/selenium-project" "./custom_training.json"

El agente analizará:
• Page Objects (*.java, *.py, *.js)
• Tests (test_*.*, *Test.*, *.spec.*)
• Step Definitions (Cucumber steps)
• Utilities y helpers
• Archivos .feature

Después del entrenamiento, el agente generará código específico
para tu proyecto usando SOLO los patrones encontrados.
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    
    project_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        success = train_with_project(project_path, output_path)
        if success:
            print("\n🎉 ¡Entrenamiento exitoso! El agente está listo para usar.")
        else:
            print("\n❌ Error durante el entrenamiento.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
