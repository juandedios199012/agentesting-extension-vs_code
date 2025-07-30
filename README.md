
# 🤖 AgentestingMIA - Agente IA para Automatización QA

**Genera código de pruebas automáticas personalizadas usando inteligencia artificial.**

![VS Code](https://img.shields.io/badge/VS%20Code-Extension-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange)

## 🚀 ¿Qué hace AgentestingMIA?

AgentestingMIA es tu **agente de IA inteligente** que no solo genera código de pruebas, sino que **crea archivos automáticamente** en tu proyecto. Como GitHub Copilot, pero especializado en QA Automation.

**✨ Capacidades del Agente:**
- 🧠 **Genera código inteligente** basado en tu proyecto
- 📁 **Crea archivos automáticamente** cuando es necesario
- 🔍 **Analiza tu código existente** para sugerencias contextuales
- 🚀 **Frameworks soportados:** Selenium, Pytest, Playwright, Cypress, y más

**Ejemplos de prompts:**
- "Crea una clase LoginPage para Selenium" → Genera y crea el archivo automáticamente
- "Genera tests de API para el endpoint /users" → Crea archivo de tests completo
- "Crea Page Objects para mi e-commerce" → Genera múltiples archivos organizados

## ⚡ Configuración REQUERIDA (2 minutos)

> **📢 IMPORTANTE:** AgentestingMIA requiere tu propia API key de OpenAI para funcionar. Es gratis obtenerla y muy económica de usar (~$0.002 por consulta).

### Paso 1: Obtener tu API key de OpenAI

1. Ve a [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crea una cuenta gratuita (o inicia sesión)
3. Haz clic en "Create new secret key"
4. Copia la clave (comenzará con `sk-...`)

### Paso 2: Configurar tu API key

**🏆 MÉTODO RECOMENDADO: Variables de Entorno (Más Seguro)**

**Windows:**
1. **Win+R** → escribe `sysdm.cpl` → Enter
2. **Pestaña "Opciones avanzadas"** → "Variables de entorno"
3. **Agregar nueva variable del sistema:**
   - Nombre: `OPENAI_API_KEY`
   - Valor: `tu-api-key-aquí`
4. **Reinicia VS Code** completamente

**macOS/Linux:**
```bash
echo 'export OPENAI_API_KEY="tu-api-key-aquí"' >> ~/.bashrc
source ~/.bashrc
```

**📌 Alternativa: Configuración VS Code**
1. Ve a `Archivo > Preferencias > Configuración` (o `Ctrl+,`)
2. Busca "**AgentestingMIA**"
3. Pega tu API key en el campo "**Openai Api Key**"

### Paso 3: ¡Usar el Agente IA!
1. **Instala la extensión** desde el VS Code Marketplace
2. **Abre la paleta de comandos** (`Ctrl+Shift+P`)
3. **Busca:** "**Agentesting Automatización de Pruebas**"
4. **Escribe prompts inteligentes:**
   - "Crea una clase Page Object para login con Selenium"
   - "Genera tests de API REST para /users endpoint"
   - "Crea suite de pruebas para formulario de registro"

## 🤖 ¿Cómo funciona el Agente?

AgentestingMIA **analiza tu prompt** y automáticamente:
1. **Genera código inteligente** usando GPT-3.5
2. **Detecta si necesita crear archivos** (como GitHub Copilot)
3. **Crea automáticamente** los archivos en las rutas apropiadas
4. **Te notifica** qué archivos se crearon

**Ejemplo:**
```
👤 Tú: "Crea una clase LoginPage con Selenium"

🤖 Agente: 
- Genera el código de la clase
- Crea automáticamente: pages/login_page.py
- Notifica: ✅ Archivo creado automáticamente: pages/login_page.py
```

## 💰 Costos

- **Configuración:** Totalmente gratuita
- **Uso:** ~$0.002 por consulta (muy económico)
- **Tu control:** Solo pagas por lo que uses en tu cuenta OpenAI

## 🎯 Ejemplos de Prompts

```
✅ "Crear pruebas automatizadas para login de usuario"
✅ "Generar validaciones para formulario de registro"  
✅ "Pruebas de API REST para endpoint de usuarios"
✅ "Suite de pruebas para carrito de compras"
✅ "Automatizar pruebas de navegación web"
```

## 🛠️ Características

- 🧠 **IA Personalizada:** Respuestas específicas para tu proyecto
- 📝 **Código Listo:** Copy-paste directo a tu proyecto
- 🔍 **Análisis Contextual:** Detecta tus frameworks automáticamente
- 📋 **Múltiples Frameworks:** Selenium, Pytest, TestNG, y más
- 🎨 **Interfaz Moderna:** Panel elegante con historial integrado

## 🔧 Requisitos

- ✅ VS Code 1.102.0+
- ✅ Python 3.8+ (instalado en tu sistema)
- ✅ Cuenta OpenAI (gratuita) para API key

## ❓ Preguntas Frecuentes

**P: ¿Es seguro ingresar mi API key?**
R: Sí, tu API key se guarda localmente en VS Code y solo tú tienes acceso.

**P: ¿Cuánto cuesta usar OpenAI?**
R: Aproximadamente $0.002 por consulta. OpenAI ofrece créditos gratuitos iniciales.

**P: ¿Funciona sin internet?**
R: No, requiere conexión para comunicarse con OpenAI y generar respuestas personalizadas.

**P: ¿Qué pasa si no configuro mi API key?**
R: La extensión te guiará paso a paso para configurarla. ¡Es muy fácil!

## 🆘 Soporte

¿Problemas o dudas?
- 📧 Contacta al desarrollador
- 🐛 [Reportar errores](https://github.com/juandedios199012/agentesting-extension-vs_code/issues)
- 💡 [Sugerir mejoras](https://github.com/juandedios199012/agentesting-extension-vs_code/issues)

---

**¡Transforma tu proceso de testing con IA! 🚀**
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
