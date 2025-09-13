// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';
import * as path from 'path';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
// Variable global para mantener el panel persistente
let currentPanel: vscode.WebviewPanel | undefined = undefined;

export function activate(context: vscode.ExtensionContext) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "Agentesting" is now active!');

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with registerCommand
    // The commandId parameter must match the command field in package.json
    // Comando Hello World
    const disposableHello = vscode.commands.registerCommand('Agentesting.helloWorld', () => {
        vscode.window.showInformationMessage('Hello World from Agente de Automatización QA!');
    });
    context.subscriptions.push(disposableHello);

    // Comando para instalar dependencias Python automáticamente
    const disposableInstallDeps = vscode.commands.registerCommand('Agentesting.installPythonDeps', async () => {
        const terminal = vscode.window.createTerminal('Agente QA - Dependencias');
        terminal.show();
        terminal.sendText('pip install langchain langchain_community openai requests');
        vscode.window.showInformationMessage('Instalando dependencias Python del agente...');
    });
    context.subscriptions.push(disposableInstallDeps);

    // Comando para ejecutar el agente Python
    const disposableRunAgent = vscode.commands.registerCommand('Agentesting.runPythonAgent', async () => {
        const extensionPath = context.extensionPath;
        const agentPath = path.join(extensionPath, 'agent-backend', 'cli.py');
        const terminal = vscode.window.createTerminal('Agente QA');
        terminal.show();
        terminal.sendText(`python "${agentPath}" --historias "ruta/a/historias" --salida "ruta/a/salida"`);
    });
    context.subscriptions.push(disposableRunAgent);

    // Comando para mostrar panel de resultados y logs (MEJORADO CON PERSISTENCIA)
    const disposableShowPanel = vscode.commands.registerCommand('Agentesting.showResultsPanel', () => {
        // Si ya existe un panel, enfócalo en lugar de crear uno nuevo
        if (currentPanel) {
            currentPanel.reveal(vscode.ViewColumn.One);
            return;
        }

        // Crear panel con persistencia mejorada
        currentPanel = vscode.window.createWebviewPanel(
            'agenteQaResults',
            'AgentestingMIA - Agente IA',
            vscode.ViewColumn.One,
            {
                enableScripts: true,
                retainContextWhenHidden: true, // CLAVE: Mantiene el estado cuando está oculto
                localResourceRoots: [vscode.Uri.file(path.join(context.extensionPath, 'agent-backend'))]
            }
        );

        currentPanel.webview.html = getWebviewContent();

        // Limpiar referencia cuando se cierra el panel
        currentPanel.onDidDispose(() => {
            currentPanel = undefined;
        }, null, context.subscriptions);

        currentPanel.webview.onDidReceiveMessage(async message => {
            if (message.type === 'enviarPrompt') {
                // Mostrar indicador de carga
                currentPanel?.webview.postMessage({ 
                    type: 'mostrarCarga', 
                    mensaje: 'Procesando con IA...' 
                });

                const respuesta = await ejecutarAgentePython(message.prompt, message.archivoAdjunto);
                
                // Detectar si el agente quiere crear un archivo automáticamente
                const match = respuesta.match(/ARCHIVO:\s*(.*)\nCONTENIDO:\n([\s\S]*)/);
                if (match) {
                    const nombreArchivo = match[1].trim();
                    const contenido = match[2];
                    try {
                        await vscode.workspace.fs.writeFile(
                            vscode.Uri.file(path.join(vscode.workspace.rootPath || '', nombreArchivo)),
                            Buffer.from(contenido, 'utf8')
                        );
                        // Mostrar notificación en VS Code
                        vscode.window.showInformationMessage(`✅ Archivo creado automáticamente: ${nombreArchivo}`);
                        
                        // Agregar información a la respuesta
                        const respuestaConArchivo = `${respuesta}\n\n📁 **Archivo creado automáticamente:** ${nombreArchivo}`;
                        currentPanel?.webview.postMessage({ type: 'respuestaAgente', respuesta: respuestaConArchivo });
                    } catch (error) {
                        currentPanel?.webview.postMessage({ type: 'respuestaAgente', respuesta: `${respuesta}\n\n❌ Error al crear archivo: ${error}` });
                    }
                } else {
                    currentPanel?.webview.postMessage({ type: 'respuestaAgente', respuesta });
                }
            }
        });
    });
    context.subscriptions.push(disposableShowPanel);

    // Comando para mostrar guía de configuración
    const disposableSetupGuide = vscode.commands.registerCommand('Agentesting.showSetupGuide', () => {
        vscode.window.showInformationMessage(
            '🤖 AgentestingMIA - Configuración rápida:\n\n1️⃣ Obtén tu API key: platform.openai.com/api-keys\n2️⃣ Configúrala: Variable de entorno OPENAI_API_KEY (recomendado) o Archivo > Preferencias > Configuración > "AgentestingMIA"\n3️⃣ ¡Empieza a generar código de pruebas con IA!',
            'Variables de Entorno',
            'Configuración VS Code',
            'Obtener API Key',
            'Abrir Panel'
        ).then(selection => {
            if (selection === 'Variables de Entorno') {
                vscode.window.showInformationMessage(
                    'Configuración por Variables de Entorno (RECOMENDADO):\n\n1️⃣ Presiona Win+R\n2️⃣ Escribe: sysdm.cpl\n3️⃣ Pestaña "Opciones avanzadas"\n4️⃣ "Variables de entorno"\n5️⃣ Agregar nueva: OPENAI_API_KEY\n6️⃣ Reinicia VS Code',
                    'Obtener API Key'
                ).then(sel => {
                    if (sel === 'Obtener API Key') {
                        vscode.env.openExternal(vscode.Uri.parse('https://platform.openai.com/api-keys'));
                    }
                });
            } else if (selection === 'Configuración VS Code') {
                vscode.commands.executeCommand('workbench.action.openSettings', 'agentestingmia.openaiApiKey');
            } else if (selection === 'Obtener API Key') {
                vscode.env.openExternal(vscode.Uri.parse('https://platform.openai.com/api-keys'));
            } else if (selection === 'Abrir Panel') {
                vscode.commands.executeCommand('Agentesting.showResultsPanel');
            }
        });
    });
    context.subscriptions.push(disposableSetupGuide);
}

function getWebviewContent(): string {
    return `
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', Arial, sans-serif;
                background: linear-gradient(135deg, #232526 0%, #414345 100%);
                color: #e0e0e0;
                padding: 0;
                margin: 0;
            }
            .container {
                max-width: 800px;
                margin: 40px auto;
                background: rgba(34, 40, 49, 0.95);
                border-radius: 16px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                padding: 32px;
            }
            h2 {
                color: #00e6fe;
                font-weight: 700;
                letter-spacing: 2px;
                margin-bottom: 16px;
            }
            .prompt-area {
                display: flex;
                flex-direction: column;
                gap: 12px;
                margin-bottom: 24px;
            }
            textarea {
                width: 100%;
                min-height: 80px;
                border-radius: 8px;
                border: none;
                padding: 12px;
                font-size: 1rem;
                background: #23272f;
                color: #e0e0e0;
                resize: vertical;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            }
            .drop-zone {
                border: 2px dashed #00e6fe;
                border-radius: 8px;
                padding: 24px;
                text-align: center;
                color: #00e6fe;
                background: #23272f;
                margin-bottom: 12px;
                transition: all 0.2s;
                cursor: pointer;
            }
            .drop-zone.dragover {
                background: #1a1d23;
                border-color: #00ff88;
                transform: scale(1.02);
            }
            .drop-zone.has-file {
                background: #1a2d1a;
                border-color: #00ff88;
                color: #00ff88;
            }
            .file-info {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                font-size: 0.9rem;
            }
            .remove-file {
                background: #ff4444;
                color: white;
                border: none;
                border-radius: 50%;
                width: 20px;
                height: 20px;
                cursor: pointer;
                font-size: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            button {
                background: linear-gradient(90deg, #00e6fe 0%, #007acc 100%);
                color: #fff;
                border: none;
                padding: 10px 24px;
                border-radius: 8px;
                font-size: 1rem;
                font-weight: 700;
                cursor: pointer;
                margin-right: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.12);
                transition: background 0.2s;
            }
            button:hover {
                background: linear-gradient(90deg, #007acc 0%, #00e6fe 100%);
            }
            .result-card {
                background: #23272f;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.10);
            }
            .result-header {
                color: #00e6fe;
                font-size: 1.1rem;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .result-content {
                white-space: pre-wrap;
                font-family: 'Fira Mono', 'Consolas', monospace;
                color: #e0e0e0;
                background: #181a20;
                border-radius: 6px;
                padding: 12px;
                margin-bottom: 8px;
            }
            .copy-btn {
                background: #00e6fe;
                color: #23272f;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 0.9rem;
                cursor: pointer;
                float: right;
                margin-top: -32px;
                margin-right: 8px;
            }
            .history {
                margin-top: 32px;
            }
            .history-header {
                color: #00e6fe;
                font-size: 1rem;
                font-weight: 700;
                margin-bottom: 8px;
            }
            .history-list {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .history-item {
                background: #23272f;
                color: #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                margin-bottom: 6px;
                font-size: 0.95rem;
                cursor: pointer;
                transition: background 0.2s;
            }
            .history-item:hover {
                background: #181a20;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Agente QA Automation <span style="font-size:1.2rem; color:#fff; background:linear-gradient(90deg,#00e6fe,#007acc); border-radius:6px; padding:2px 10px;">AI</span></h2>
            <div class="prompt-area">
                <form id="promptForm">
                    <label for="prompt">Escribe tu historia, prompt o arrastra un archivo:</label><br>
                    <textarea id="prompt" placeholder="Como usuario quiero..."></textarea><br>
                    <div id="dropZone" class="drop-zone">Arrastra aquí archivos para analizar</div>
                    <button type="submit">Enviar al agente</button>
                </form>
            </div>
            <div class="result-card">
                <div class="result-header">Respuesta del agente:</div>
                <button class="copy-btn" onclick="copyRespuesta()">Copiar</button>
                <div id="respuesta" class="result-content">(Aquí aparecerá la respuesta...)</div>
            </div>
            <div class="history">
                <div class="history-header">Historial de prompts</div>
                <ul id="historyList" class="history-list"></ul>
            </div>
        </div>
        <script>
            const vscode = acquireVsCodeApi();
            
            // PERSISTENCIA: Recuperar estado anterior si existe
            const previousState = vscode.getState() || {};
            let history = previousState.history || [];
            let archivoAdjunto = previousState.archivoAdjunto || null;
            let isLoading = false;
            
            // Restaurar historial al cargar
            if (history.length > 0) {
                renderHistory();
            }
            
            // Restaurar archivo adjunto si existe
            if (archivoAdjunto) {
                updateDropZone();
            }
            
            document.getElementById('promptForm').addEventListener('submit', function(e) {
                e.preventDefault();
                if (isLoading) return; // Prevenir envíos múltiples
                
                const prompt = document.getElementById('prompt').value;
                if (!prompt.trim()) return;
                
                addToHistory(prompt);
                setLoadingState(true);
                
                vscode.postMessage({ 
                    type: 'enviarPrompt', 
                    prompt,
                    archivoAdjunto 
                });
            });
            
            function setLoadingState(loading) {
                isLoading = loading;
                const button = document.querySelector('button[type="submit"]');
                const respuesta = document.getElementById('respuesta');
                
                if (loading) {
                    button.textContent = 'Procesando...';
                    button.disabled = true;
                    respuesta.textContent = '🤖 AgentestingMIA está procesando tu solicitud...';
                    respuesta.style.color = '#00e6fe';
                    respuesta.style.fontStyle = 'italic';
                } else {
                    button.textContent = 'Enviar al agente';
                    button.disabled = false;
                    respuesta.style.color = '#e0e0e0';
                    respuesta.style.fontStyle = 'normal';
                }
            }
            
            function addToHistory(prompt) {
                history.unshift(prompt);
                if (history.length > 20) history = history.slice(0, 20); // Limitar historial
                saveState();
                renderHistory();
            }
            
            function saveState() {
                vscode.setState({
                    history: history,
                    archivoAdjunto: archivoAdjunto
                });
            }
            
            function renderHistory() {
                const list = document.getElementById('historyList');
                list.innerHTML = '';
                history.slice(0,10).forEach(item => {
                    const li = document.createElement('li');
                    li.className = 'history-item';
                    li.textContent = item;
                    li.onclick = () => {
                        document.getElementById('prompt').value = item;
                    };
                    list.appendChild(li);
                });
            }
            
            function copyRespuesta() {
                const respuesta = document.getElementById('respuesta').textContent;
                navigator.clipboard.writeText(respuesta);
            }
            
            function removeFile() {
                archivoAdjunto = null;
                saveState();
                updateDropZone();
            }
            
            function updateDropZone() {
                const dropZone = document.getElementById('dropZone');
                if (archivoAdjunto) {
                    dropZone.classList.add('has-file');
                    dropZone.innerHTML = 
                        '<div class="file-info">' +
                            '📁 ' + archivoAdjunto.nombre + ' (' + Math.round(archivoAdjunto.contenido.length / 1024) + 'KB)' +
                            '<button class="remove-file" onclick="removeFile()" title="Quitar archivo">×</button>' +
                        '</div>';
                } else {
                    dropZone.classList.remove('has-file');
                    dropZone.innerHTML = 'Arrastra aquí archivos para analizar';
                }
            }
            
            // Drag & drop archivos mejorado
            const dropZone = document.getElementById('dropZone');
            
            dropZone.addEventListener('click', () => {
                if (archivoAdjunto) {
                    removeFile();
                }
            });
            
            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            });
            
            dropZone.addEventListener('dragleave', (e) => {
                dropZone.classList.remove('dragover');
            });
            
            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                const files = e.dataTransfer.files;
                
                if (files.length > 0) {
                    const file = files[0];
                    const reader = new FileReader();
                    
                    reader.onload = function(evt) {
                        archivoAdjunto = {
                            nombre: file.name,
                            contenido: evt.target.result,
                            tipo: file.type
                        };
                        saveState();
                        updateDropZone();
                        
                        // Auto-generar prompt si está vacío
                        const promptField = document.getElementById('prompt');
                        if (!promptField.value.trim()) {
                            promptField.value = 'Analiza este archivo y sugiere mejoras basándote en los patrones del proyecto:\\n\\nArchivo: ' + file.name;
                        }
                    };
                    
                    reader.readAsText(file);
                }
            });
            
            window.addEventListener('message', event => {
                const message = event.data;
                if (message.type === 'respuestaAgente') {
                    setLoadingState(false);
                    document.getElementById('respuesta').textContent = message.respuesta;
                    
                    // Mostrar notificación si se creó un archivo automáticamente
                    if (message.respuesta.includes('Archivo creado/modificado automáticamente:')) {
                        const respuestaElement = document.getElementById('respuesta');
                        respuestaElement.style.borderLeft = '4px solid #00ff88';
                        setTimeout(() => {
                            respuestaElement.style.borderLeft = 'none';
                        }, 3000);
                    }
                    
                    // Limpiar archivo adjunto después de procesar
                    if (archivoAdjunto) {
                        archivoAdjunto = null;
                        saveState();
                        updateDropZone();
                    }
                } else if (message.type === 'mostrarCarga') {
                    setLoadingState(true);
                }
            });
        </script>
    </body>
    </html>
    `;
}

// This method is called when your extension is deactivated
export function deactivate() {}

// Helper para obtener extensión de archivo
function getFileExtension(filename: string): string {
    const ext = filename.split('.').pop()?.toLowerCase();
    switch(ext) {
        case 'java': return 'java';
        case 'py': return 'python';
        case 'js': return 'javascript';
        case 'ts': return 'typescript';
        case 'feature': return 'gherkin';
        default: return 'text';
    }
}

// Ejecuta el agente Python embebido en la extensión y retorna la respuesta (OPTIMIZADO)
async function ejecutarAgentePython(prompt: string, archivoAdjunto?: any): Promise<string> {
    const { exec } = require('child_process');
    const fs = require('fs');
    const path = require('path');
    
    // Usa la ruta interna del backend embebido en la extensión (TEMPORAL - DIAGNÓSTICO)
    const extensionPath = vscode.extensions.getExtension('AgentestingMIA.agentestingmia')?.extensionPath || __dirname;
    const agentPath = path.join(extensionPath, 'out', 'agent-backend', 'test_agent.py'); // TEMPORAL: usar test_agent para diagnosticar
    const workspaceRoot = vscode.workspace.rootPath || process.cwd();
    
    // Busca la API key en orden de prioridad:
    // 1. Variable de entorno del sistema (más limpio y seguro)
    // 2. Configuración de VS Code (backup)
    let userApiKey = process.env.OPENAI_API_KEY;
    if (!userApiKey) {
        const config = vscode.workspace.getConfiguration('agentestingmia');
        userApiKey = config.get<string>('openaiApiKey');
    }
    
    // Si no hay API key configurada, muestra mensaje informativo
    if (!userApiKey || !userApiKey.trim()) {
        vscode.window.showErrorMessage(
            '🔑 AgentestingMIA requiere tu API key de OpenAI para funcionar. ¡Configúrala fácilmente!',
            'Variables de Entorno (Recomendado)', 
            'Configuración VS Code',
            'Obtener API Key'
        ).then(selection => {
            if (selection === 'Variables de Entorno (Recomendado)') {
                vscode.window.showInformationMessage(
                    'Configuración por Variables de Entorno (MÁS SEGURO):\n\n1️⃣ Presiona Win+R\n2️⃣ Escribe: sysdm.cpl\n3️⃣ Pestaña "Opciones avanzadas"\n4️⃣ "Variables de entorno"\n5️⃣ Agregar nueva: OPENAI_API_KEY\n6️⃣ Reinicia VS Code',
                    'Obtener API Key'
                ).then(sel => {
                    if (sel === 'Obtener API Key') {
                        vscode.env.openExternal(vscode.Uri.parse('https://platform.openai.com/api-keys'));
                    }
                });
            } else if (selection === 'Configuración VS Code') {
                vscode.commands.executeCommand('workbench.action.openSettings', 'agentestingmia.openaiApiKey');
            } else if (selection === 'Obtener API Key') {
                vscode.env.openExternal(vscode.Uri.parse('https://platform.openai.com/api-keys'));
            }
        });
        
        // Retorna mensaje explicativo incluso sin API key
        return Promise.resolve(`🔑 **AgentestingMIA necesita tu API key de OpenAI**

📝 **Tu solicitud:** "${prompt}"

⚡ **Configuración RECOMENDADA (Variables de Entorno):**

**Windows:**
1. **Win+R** → escribe \`sysdm.cpl\`
2. **Pestaña "Opciones avanzadas"** → "Variables de entorno"
3. **Agregar nueva variable:**
   - Nombre: \`OPENAI_API_KEY\`
   - Valor: \`tu-api-key-aquí\`
4. **Reiniciar VS Code**

**Alternativa (VS Code):**
- Archivo > Preferencias > Configuración > "AgentestingMIA"

💰 **Costo:** ~$0.002 por consulta (muy económico)
🧠 **Beneficios:** Variables de entorno son más seguras y limpias`);
    }
    
    return new Promise((resolve) => {
        // Prepara el prompt completo incluyendo archivo adjunto si existe (OPTIMIZADO)
        let promptCompleto = prompt;
        
        if (archivoAdjunto) {
            promptCompleto = `${prompt}

📁 **ARCHIVO ADJUNTO: ${archivoAdjunto.nombre}**

\`\`\`${getFileExtension(archivoAdjunto.nombre)}
${archivoAdjunto.contenido}
\`\`\`

INSTRUCCIONES:
1. Analiza el código adjunto basándote en el entrenamiento especializado del proyecto
2. Identifica patrones móviles (Appium) o web (Selenium)  
3. Sugiere mejoras específicas usando la arquitectura Task-Screen/Page-Control
4. Propón código optimizado siguiendo los estándares detectados`;
        }
        
        // Prepara el entorno con la API key del usuario
        const env = { 
            ...process.env,
            OPENAI_API_KEY: userApiKey || ''
        };
        
        // OPTIMIZACIÓN: Usar timeout y límite de memoria
        const options = {
            cwd: workspaceRoot,
            env: env,
            timeout: 30000, // 30 segundos máximo
            maxBuffer: 1024 * 1024 // 1MB máximo de salida
        };
        
        exec(`python "${agentPath}" "${promptCompleto.replace(/"/g, '\\"')}"`, options, (error: any, stdout: string, stderr: string) => {
            if (error) {
                if (error.code === 'TIMEOUT') {
                    resolve('❌ **Timeout**: El agente tardó más de 30 segundos. Intenta con un prompt más específico.');
                } else {
                    // DIAGNÓSTICO MEJORADO: Mostrar más información del error
                    const errorInfo = `❌ **Error del agente**: 
**Código de error:** ${error.code || 'N/A'}
**Mensaje:** ${error.message || 'N/A'}
**STDERR:** ${stderr || 'N/A'}
**Ruta del agente:** ${agentPath}
**Directorio de trabajo:** ${workspaceRoot}

💡 **Sugerencias:**
- Verifica que Python esté instalado y en el PATH
- Revisa la configuración de la API key
- Intenta con un prompt más simple
- Consulta la consola de VS Code para más detalles`;
                    resolve(errorInfo);
                }
            } else {
                const respuesta = stdout.trim();
                if (respuesta.includes('[SUCCESS]')) {
                    resolve(respuesta.replace('[SUCCESS]', '✅ **[SUCCESS]**'));
                } else if (respuesta.length === 0) {
                    resolve('⚠️ **El agente no devolvió respuesta**. Esto puede indicar:\n- Problemas con las dependencias de Python\n- Error en la configuración de la API key\n- El agente se ejecutó pero no generó salida\n\nVerifica la consola de VS Code para más detalles.');
                } else {
                    resolve(respuesta || '⚠️ El agente ejecutó pero no devolvió contenido válido.');
                }
            }
        });
    });
}

// Ejemplo: crear clase desde prompt del agente
async function crearClaseDesdePrompt(nombreArchivo: string, nombreClase: string, contenidoClase: string) {
    const uri = vscode.Uri.file(path.join(vscode.workspace.rootPath || '', nombreArchivo));
    const claseCode = `class ${nombreClase} {
${contenidoClase}
}`;
    await vscode.workspace.fs.writeFile(uri, Buffer.from(claseCode, 'utf8'));
}
