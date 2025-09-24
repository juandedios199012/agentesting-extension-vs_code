#!/usr/bin/env python3
"""
test_agent.py - Versión simplificada para diagnosticar problemas
"""
import sys
import os

def simple_agent_test():
    """Test simple del agente"""
    try:
    print("[DEBUG] Iniciando test del agente...")
        
        # Verificar API key
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            print("No se encontró OPENAI_API_KEY")
            return "ERROR: No hay API key configurada"
        
    print(f"API Key encontrada: {api_key[:10]}...")
        
        # Verificar LangChain
        try:
            from langchain_openai import ChatOpenAI
            print("LangChain importado correctamente")
        except ImportError as e:
            print(f"Error importando LangChain: {e}")
            return "ERROR: LangChain no disponible"
        
        # Test básico con OpenAI
        print("🤖 Iniciando test de OpenAI...")
        llm = ChatOpenAI(
            temperature=0.1,
            model_name="gpt-3.5-turbo",
            openai_api_key=api_key,
            max_tokens=200,
            request_timeout=10
        )
        
        # Obtener prompt del argumento
        if len(sys.argv) > 1:
            prompt = sys.argv[1]
        else:
            prompt = "Hola, ¿puedes ayudarme con automatización móvil?"
        
        print(f"📝 Prompt recibido: {prompt}")
        
        # Generar respuesta
        from langchain_core.messages import HumanMessage
        response = llm.invoke([HumanMessage(content=f"""
Eres AgentestingMIA, un especialista en automatización de pruebas móviles con Appium y web con Selenium.

PROMPT DEL USUARIO: {prompt}

Responde de forma específica y práctica. Si piden automatización móvil, sugiere clases específicas como LoginScreen, CarritoScreen, etc.
""")])
        
        result = response.content if hasattr(response, 'content') else str(response)
    print("Respuesta generada exitosamente")
        return result
        
    except Exception as e:
        error_msg = f"❌ Error en test: {str(e)}"
        print(error_msg)
        return error_msg

if __name__ == "__main__":
    result = simple_agent_test()
    print("\n" + "="*50)
    print("RESPUESTA FINAL:")
    print("="*50)
    print(result)
