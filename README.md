
# Agentesting - Extensión VS Code para Automatización QA

## Instalación y Primeros Pasos

1. **Instala la extensión desde el Marketplace o VSIX.**
2. **Instala las dependencias Python del backend:**
   - Abre la paleta de comandos (`Ctrl+Shift+P`)
   - Ejecuta: `Agentesting: Instalar dependencias Python`

   - Esto instalará automáticamente todos los paquetes necesarios para el agente, incluyendo:
     - `langchain`
     - `langchain_community`
     - `openai`
     - `azure-identity`
     - `azure-keyvault-secrets`
     - `requests`
   - No necesitas preocuparte por rutas ni archivos adicionales, solo ejecuta el comando y el entorno estará listo.


> Alternativamente, puedes instalar manualmente:
> ```powershell
> pip install langchain openai azure-identity azure-keyvault-secrets requests
> ```

3. **Abre el panel del agente:**
   - Ejecuta: `Agentesting: Automatización de Pruebas`
   - Usa el área de prompt para escribir historias, preguntas o arrastrar archivos.
   - Visualiza respuestas, código generado y logs en tiempo real.

## Características
- Generación de artefactos y código contextual usando IA.
- Aprendizaje incremental: el agente mejora con el uso y entrenamiento.
- UI moderna y elegante, con historial, drag & drop y acciones rápidas.
- Integración total con tu workspace y frameworks detectados.

## Requisitos
- Python 3.8+
- Acceso a internet para modelos LLM (OpenAI)

## Soporte
Para dudas, sugerencias o soporte, contacta al publisher o abre un issue en el repositorio.

### Configuración
La extensión puede agregar configuraciones para rutas de historias, salida de artefactos y parámetros de ejecución del agente.

## Known Issues

### Problemas conocidos
- El agente Python debe estar correctamente configurado y accesible desde la extensión.
- Las credenciales LLM deben definirse en `.env` para funciones avanzadas.

## Release Notes

### 1.0.0
- Versión inicial: ejecución del agente Python, panel webview, integración básica y documentación.

### 1.0.1

Fixed issue #.

### 1.1.0

Added features X, Y, and Z.

---

## Following extension guidelines

Ensure that you've read through the extensions guidelines and follow the best practices for creating your extension.

* [Extension Guidelines](https://code.visualstudio.com/api/references/extension-guidelines)

## Working with Markdown

You can author your README using Visual Studio Code. Here are some useful editor keyboard shortcuts:

* Split the editor (`Cmd+\` on macOS or `Ctrl+\` on Windows and Linux).
* Toggle preview (`Shift+Cmd+V` on macOS or `Shift+Ctrl+V` on Windows and Linux).
* Press `Ctrl+Space` (Windows, Linux, macOS) to see a list of Markdown snippets.

## For more information

* [Visual Studio Code's Markdown Support](http://code.visualstudio.com/docs/languages/markdown)
* [Markdown Syntax Reference](https://help.github.com/articles/markdown-basics/)

**Enjoy!**
