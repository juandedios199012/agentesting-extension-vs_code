#!/usr/bin/env python3
"""
Script de diagnóstico para AgentestingMIA
Verifica si la API key está configurada correctamente
"""

import os
import sys

def check_api_key():
    print("=== DIAGNÓSTICO AgentestingMIA ===")
    print()
    
    # 1. Verificar variable de entorno
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key:
        print("✓ Variable de entorno OPENAI_API_KEY: CONFIGURADA")
        if env_key.startswith('sk-'):
            print("✓ Formato de API key: CORRECTO (comienza con 'sk-')")
        else:
            print("✗ Formato de API key: INCORRECTO (debe comenzar con 'sk-')")
        print(f"  Primeros caracteres: {env_key[:10]}...")
        print(f"  Longitud: {len(env_key)} caracteres")
    else:
        print("✗ Variable de entorno OPENAI_API_KEY: NO CONFIGURADA")
    
    print()
    
    # 2. Verificar argumentos de línea de comandos
    if len(sys.argv) > 1:
        print("✓ Argumentos recibidos:", sys.argv[1:])
    else:
        print("- Sin argumentos adicionales")
    
    print()
    
    # 3. Verificar archivo de configuración
    config_file = os.path.join(os.path.dirname(__file__), 'config.txt')
    if os.path.exists(config_file):
        print("✓ Archivo config.txt: EXISTE")
    else:
        print("- Archivo config.txt: NO EXISTE (opcional)")
    
    print()
    print("=== RECOMENDACIONES ===")
    if not env_key:
        print("1. Configura tu variable de entorno OPENAI_API_KEY:")
        print("   - Win+R -> sysdm.cpl -> Variables de entorno")
        print("   - Agregar: OPENAI_API_KEY = tu-api-key")
        print("   - Reiniciar VS Code")
        print()
        print("2. Obtén tu API key en: https://platform.openai.com/api-keys")
    else:
        print("✓ Tu configuración parece correcta!")

if __name__ == '__main__':
    check_api_key()
