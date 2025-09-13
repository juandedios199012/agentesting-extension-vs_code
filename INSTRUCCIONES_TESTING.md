# 🧪 Instrucciones para Probar AgentestingMIA

## 🎯 Estado Actual
- ✅ Backend ejecutándose correctamente
- ✅ Extensión compilada sin errores
- ✅ Workspace limpio (proyecto de ejemplo eliminado)
- ✅ Drag & drop mejorado implementado

## 🚀 Pasos para Probar

### 1. **Abrir la Extensión**
1. **En VS Code actual:** Presiona `F5` (abrirá nueva ventana de desarrollo)
2. **En la nueva ventana:** Presiona `Ctrl+Shift+P`
3. **Buscar:** `AgentestingMIA: Analizar Código`
4. **Seleccionar** el comando para abrir la webview

### 2. **Archivos Disponibles para Testing**
- 📁 `test-file-to-analyze.java` (optimizado para pruebas)
- 📁 `LoginPage.java` (ejemplo básico)
- 📁 Archivos del proyecto `FlexBusinessMobile-test-ui-with-ai/*`

### 3. **Probar Drag & Drop**
1. **Arrastrar archivo** a la zona de drop en la webview
2. **Verificar feedback visual:**
   - ✅ Nombre del archivo
   - ✅ Tamaño del archivo
   - ✅ Indicador de archivo adjunto
3. **Auto-prompt generado:** Se debe mostrar sugerencia automática

### 4. **Probar Análisis**
1. **Hacer clic** en "Analizar código"
2. **Verificar respuesta del agente:**
   - ✅ Análisis basado en entrenamiento especializado
   - ✅ Sugerencias específicas para testing
   - ✅ Patrones del proyecto FlexBusinessMobile

## 🔧 Funcionalidades Implementadas

### **Drag & Drop Mejorado**
- **Antes:** Los archivos se abrían en lugar de adjuntarse
- **Ahora:** Los archivos se adjuntan correctamente para análisis
- **Visual feedback:** Muestra información del archivo adjunto

### **Auto-prompt**
- **Generación automática** de sugerencias de análisis
- **Contexto específico** basado en el tipo de archivo
- **Integración** con el entrenamiento del proyecto

### **Análisis Especializado**
- **Entrenamiento híbrido:** Soporte para móvil y web
- **Patrones específicos:** Basado en FlexBusinessMobile
- **Sugerencias contextuales:** Optimizaciones específicas para testing

## 🎯 Qué Esperar

### **Al arrastrar `test-file-to-analyze.java`:**
```
📁 test-file-to-analyze.java (1KB)
✅ Archivo adjunto correctamente

Auto-prompt sugerido:
"Analiza este código de Page Object Pattern y sugiere mejoras 
para optimización de testing automatizado"
```

### **Respuesta del agente:**
- Análisis del patrón Page Object
- Sugerencias de mejoras específicas
- Recomendaciones basadas en el proyecto FlexBusinessMobile
- Patrones de testing automatizado optimizados

## 📋 Checklist de Testing

- [ ] Extensión abre correctamente (F5 → Ctrl+Shift+P → AgentestingMIA)
- [ ] Webview se muestra con zona de drag & drop
- [ ] Arrastrar archivo muestra feedback visual
- [ ] Auto-prompt se genera automáticamente
- [ ] Análisis funciona y devuelve respuesta del agente
- [ ] Respuesta contiene sugerencias específicas y contextuales

## 🛠️ Troubleshooting

### **Si la extensión no aparece:**
- Verificar que F5 inició correctamente
- Revisar que no hay errores de compilación
- Comprobar que el backend esté ejecutándose

### **Si drag & drop no funciona:**
- Verificar que el archivo sea de tipo soportado (.java, .js, .ts, etc.)
- Intentar con `test-file-to-analyze.java`
- Revisar consola del webview (F12)

### **Si el análisis no responde:**
- Verificar que el backend esté ejecutándose (puerto local)
- Comprobar logs del terminal del backend
- Intentar reiniciar el backend

---

## 🎉 **¡Listo para Probar!**

El sistema está completamente configurado y listo para testing. 
Todos los componentes están funcionando correctamente.
