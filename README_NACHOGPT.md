# 🤖 NachoGPT - Asistente de IA

## 📋 Descripción

**NachoGPT** es un asistente de IA personal que puede analizar documentos y responder preguntas sobre ellos. Está diseñado para funcionar completamente offline usando el modelo **oss20B** a través de Ollama, proporcionando una interfaz web estilo ChatGPT.

## ✨ Características Principales

- 🤖 **Modelo Local**: Usa el modelo **oss20B** de Ollama (completamente offline)
- 📄 **Procesamiento Universal**: Lee cualquier tipo de archivo (PDF, Excel, Word, TXT, CSV, etc.)
- 🌐 **Interfaz Web**: Interfaz estilo ChatGPT con Streamlit
- 🔍 **Análisis Inteligente**: Analiza documentos y responde preguntas específicas
- 📊 **Datos Estructurados**: Procesa archivos Excel y CSV con análisis detallado
- 🚀 **Una Instancia**: Se abre solo una vez en el navegador

### 🎨 **Interfaz Estilo ChatGPT**
- **Diseño familiar**: Interfaz similar a ChatGPT
- **Tema oscuro**: Colores y estilos modernos
- **Responsive**: Se adapta a diferentes tamaños de pantalla
- **Una sola instancia**: Solo abre una ventana del navegador

### 🚀 **Funcionalidades**
- ✅ **Chat inteligente**: Conversaciones naturales en español
- ✅ **Análisis de documentos**: Excel, PDF, Word, TXT, CSV, MD
- ✅ **Procesamiento directo**: Sin vector store complejo
- ✅ **Modelo optimizado**: llama2 para mejor rendimiento
- ✅ **Búsqueda inteligente**: Encuentra información relevante

### 🔧 **Características Técnicas**
- **Procesamiento completo**: Extrae toda la información de los documentos
- **Búsqueda por palabras clave**: Encuentra documentos relacionados
- **Respuestas estructuradas**: Análisis, resultados, conclusiones y recomendaciones
- **Gestión de documentos**: Vista previa y estadísticas

## 🛠️ Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- Ollama instalado ([Descargar aquí](https://ollama.ai))

### Instalación Automática

#### Windows
```bash
# Ejecutar el archivo batch
iniciar_nachogpt.bat
```

#### Linux/Mac
```bash
# Ejecutar el script Python
python run_nachogpt.py
```

### Instalación Manual
```bash
# 1. Clonar o descargar el proyecto
# 2. Instalar dependencias
pip install streamlit langchain-ollama pandas PyPDF2 python-docx openpyxl python-dotenv

# 3. Instalar modelo llama2
ollama pull llama2

# 4. Ejecutar
python run_nachogpt.py
```

## 📁 Estructura del Proyecto

```
Chatbot/
├── app_nachogpt.py              # Aplicación NachoGPT
├── run_nachogpt.py              # Script de ejecución
├── simple_ai_assistant.py       # Asistente IA simplificado
├── document_processor.py        # Procesador de documentos
├── config.py                    # Configuración
├── contexto/                    # Carpeta para documentos
├── iniciar_nachogpt.bat         # Script Windows
├── requirements.txt             # Dependencias
├── .gitignore                   # Configuración Git
└── README_NACHOGPT.md           # Este archivo
```

## 🚀 Uso de NachoGPT

### 1. **Preparación de Documentos**
Coloca tus documentos en la carpeta `contexto/`:
- 📊 **Excel**: `.xlsx`, `.csv`
- 📄 **PDF**: `.pdf`
- 📝 **Word**: `.docx`
- 📋 **Texto**: `.txt`, `.md`

### 2. **Iniciar NachoGPT**
```bash
# Opción 1: Script automático (Windows)
iniciar_nachogpt.bat

# Opción 2: Python directo
python run_nachogpt.py
```

### 3. **Usar la Interfaz**
- 🌐 Abrir: http://localhost:8501
- 💬 **Chat**: Conversaciones naturales
- 📊 **Análisis**: Consultas detalladas
- ⚙️ **Sidebar**: Configuración y estadísticas

## 💬 Ejemplos de Uso

### Chat Simple
```
Usuario: ¿Cuáles son las políticas de la empresa?
NachoGPT: Las políticas de la empresa incluyen...

Usuario: ¿Cuál es el producto más vendido?
NachoGPT: Según los datos históricos, el producto más vendido es...
```

### Análisis Detallado
```
Consulta: ¿Cuál es el producto más vendido según los datos históricos?

RESULTADO:
1. ANÁLISIS: [Análisis detallado de los datos]
2. RESULTADOS: [Números específicos y rankings]
3. CONCLUSIONES: [Conclusiones basadas en datos]
4. RECOMENDACIONES: [Recomendaciones específicas]
5. FUENTES: [Archivos utilizados]
```

## 🎯 Características de la Interfaz

### 🎨 **Diseño Visual**
- **Header verde**: Estilo ChatGPT con gradiente
- **Tema oscuro**: Colores #343541, #444654
- **Tipografía moderna**: Fuentes claras y legibles
- **Botones estilizados**: Verde #10a37f

### 📱 **Experiencia de Usuario**
- **Sidebar colapsable**: Configuración accesible
- **Chat fluido**: Mensajes bien organizados
- **Input intuitivo**: Campo de texto prominente
- **Pestañas claras**: Chat y Análisis separados

### ⚙️ **Funcionalidades**
- **Reprocesar documentos**: Actualizar contenido
- **Estadísticas en tiempo real**: Documentos y mensajes
- **Limpiar chat**: Reiniciar conversación
- **Vista previa de documentos**: Información detallada

## 🔄 Comparación con ChatGPT

| Característica | NachoGPT | ChatGPT |
|----------------|----------|---------|
| **Interfaz** | ✅ Estilo ChatGPT | ✅ Original |
| **Modelo** | llama2 (local) | GPT-4 (nube) |
| **Documentos** | ✅ Análisis local | ❌ Limitado |
| **Privacidad** | ✅ 100% local | ❌ Datos en nube |
| **Costo** | ✅ Gratis | ❌ Pago |
| **Velocidad** | ✅ Rápido | ⚠️ Depende de conexión |

## 🎯 Casos de Uso Ideales

### ✅ **NachoGPT es Perfecto para:**
- **Análisis de documentos**: Excel, PDF, Word
- **Consultas sobre políticas**: Manuales, procedimientos
- **Análisis de datos**: Reportes, estadísticas
- **Investigación**: Documentos técnicos, informes
- **Privacidad**: Datos sensibles que no pueden ir a la nube

### 🚀 **Ventajas Clave:**
- **Procesamiento local**: Sin envío de datos a servidores externos
- **Sin límites**: No hay restricciones de uso
- **Personalizable**: Puedes ajustar el modelo y configuración
- **Offline**: Funciona sin conexión a internet

## 🔧 Configuración Avanzada

### Cambiar Modelo
Editar `config.py`:
```python
OLLAMA_MODEL = "llama2"  # Modelo actual
# OLLAMA_MODEL = "gpt-oss:20b"  # Modelo más potente
```

### Ajustar Parámetros
```python
# En config.py
MAX_TOKENS = 4000        # Máximo de tokens
TEMPERATURE = 0.7        # Creatividad (0.0-1.0)
```

## 🐛 Solución de Problemas

### Error: "Ollama no está ejecutándose"
```bash
# 1. Instalar Ollama
# 2. Ejecutar: ollama serve
# 3. Descargar modelo: ollama pull llama2
```

### Error: "Modelo no encontrado"
```bash
# Descargar el modelo
ollama pull llama2
```

### Error: "Dependencias faltantes"
```bash
# Instalar dependencias
pip install streamlit langchain-ollama pandas PyPDF2 python-docx openpyxl python-dotenv
```

### Error: "Puerto 8501 ocupado"
```bash
# Cambiar puerto en run_nachogpt.py
# Buscar "--server.port", "8501" y cambiar a otro puerto
```

## 📈 Ventajas de NachoGPT

### 🚀 **Rendimiento**
- **Inicio rápido**: Sin carga de vector store complejo
- **Respuesta inmediata**: Procesamiento directo
- **Menor latencia**: Sin búsqueda compleja

### 💾 **Recursos**
- **Menos memoria**: Sin embeddings complejos
- **CPU eficiente**: Procesamiento ligero
- **Disco mínimo**: Sin archivos de vector store

### 🔒 **Privacidad**
- **100% local**: No se envían datos a servidores externos
- **Sin tracking**: No hay seguimiento de uso
- **Control total**: Tú controlas todos los datos

## 🤝 Contribuir

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Haz commit de tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas:
1. Revisa la sección de solución de problemas
2. Verifica que Ollama esté funcionando
3. Asegúrate de tener el modelo llama2 descargado
4. Revisa los logs en la consola

## 🎉 ¡Disfruta NachoGPT!

**NachoGPT** te ofrece una experiencia similar a ChatGPT pero con el poder de analizar tus documentos locales de manera privada y eficiente.

---

**🤖 NachoGPT** - Tu asistente de IA personal con interfaz estilo ChatGPT.
