
# 🤖 AgentestingMIA - Agente IA para Automatización QA

**Genera código de pruebas automáticas personalizadas usando inteligencia artificial.**

![VS Code](https://img.shields.io/badge/VS%20Code-Extension-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange)

## 🚀 ¿Qué hace AgentestingMIA?

AgentestingMIA es tu asistente personal de IA que genera código de pruebas automatizadas específicamente para tu proyecto. Solo describe lo que quieres probar y obtén código listo para usar con frameworks como Selenium, Pytest, y más.

**Ejemplos de lo que puedes generar:**
- Pruebas de login automatizadas
- Validación de formularios
- Pruebas de API REST
- Casos de navegación web
- Suites de pruebas completas

## ⚡ Configuración Rápida (2 minutos)

### Paso 1: Instalar la extensión
1. Busca "AgentestingMIA" en el marketplace de VS Code
2. Haz clic en "Install"

### Paso 2: Configurar tu API key de OpenAI

**🔑 ¿Qué es esto?** Tu API key te permite acceder a GPT-3.5 para generar respuestas personalizadas.

**📍 ¿Dónde conseguir tu API key?**
1. Ve a [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Crea una cuenta gratuita (o inicia sesión)
3. Haz clic en "Create new secret key"
4. Copia la clave (comenzará con `sk-...`)

**⚙️ ¿Cómo configurarla?**

**🏆 RECOMENDADO: Variables de Entorno (Más Seguro)**

*Windows:*
1. **Win+R** → escribe `sysdm.cpl` → Enter
2. **Pestaña "Opciones avanzadas"** → "Variables de entorno"
3. **Agregar nueva variable del sistema:**
   - Nombre: `OPENAI_API_KEY`
   - Valor: `tu-api-key-aquí`
4. **Reinicia VS Code** completamente

*macOS/Linux:*
```bash
echo 'export OPENAI_API_KEY="tu-api-key-aquí"' >> ~/.bashrc
source ~/.bashrc
```

**📌 Alternativa: Configuración VS Code**
1. Ve a `Archivo > Preferencias > Configuración` (o `Ctrl+,`)
2. Busca "**AgentestingMIA**"
3. Pega tu API key en el campo "**Openai Api Key**"
4. ¡Listo! 🎉

### Paso 3: ¡Empezar a usar!
1. Abre la paleta de comandos (`Ctrl+Shift+P`)
2. Busca "**Agentesting Automatización de Pruebas**"
3. Escribe tu prompt: *"Crear pruebas de login para mi aplicación web"*
4. ¡Obtén código personalizado al instante!

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
