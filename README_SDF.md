# 🤖 SDF Assistant - Asistente IA Avanzado

Un asistente de inteligencia artificial local que utiliza Ollama para procesar y analizar documentos de manera inteligente con **búsqueda dinámica de contexto**.

## ✨ Características

- 🔍 **Búsqueda Inteligente**: Encuentra automáticamente los documentos relevantes para cada pregunta
- 🧠 **IA Local**: Utiliza modelos de Ollama sin necesidad de conexión a internet
- 📊 **Análisis Dinámico**: Solo analiza los documentos que contienen información relevante
- 🎯 **Contexto Optimizado**: Mejora la precisión al usar solo documentos pertinentes
- 💬 **Interfaz Web**: Interfaz moderna y fácil de usar con Streamlit
- 🔧 **Configurable**: Personalizable para diferentes modelos y configuraciones
- 📁 **Múltiples Formatos**: Soporta Excel, PDF, CSV, Word, Texto y más

## 🚀 Instalación Rápida

### Requisitos Previos

1. **Python 3.8 o superior**
2. **Ollama** instalado y ejecutándose
3. **Git** (para clonar el repositorio)

### Pasos de Instalación

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/Chatbot.git
cd Chatbot/SDF_Assistant
```

#### 2. Instalación Automática (Recomendado)
```bash
python setup_sdf.py
```

#### 3. Inicio Rápido
```bash
python quick_start_sdf.py
```

#### 4. Instalación Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar modelo de IA
ollama pull gpt-oss:20b

# Crear carpeta de contexto
mkdir contexto
```

## 🎯 Uso

### Ejecutar SDF Assistant

#### Opción 1: Script Python
```bash
python run_sdf.py
```

#### Opción 2: Script Batch (Windows)
```bash
iniciar_sdf.bat
```

#### Opción 3: Directo con Streamlit
```bash
streamlit run app_sdf.py
```

### Acceder a la Aplicación

1. Abre tu navegador
2. Ve a: `http://localhost:8502`
3. ¡Listo para usar!

## 📁 Estructura del Proyecto

```
SDF_Assistant/
├── 📄 app_sdf.py              # Aplicación principal
├── 🤖 sdf_assistant.py        # Lógica del asistente
├── 📊 document_processor.py   # Procesador de documentos
├── ⚙️ config.py              # Configuración
├── 🚀 run_sdf.py             # Script de ejecución
├── 📦 setup_sdf.py           # Instalador automático
├── ⚡ quick_start_sdf.py     # Inicio rápido
├── 🔍 check_system_sdf.py    # Verificación del sistema
├── 🖥️ iniciar_sdf.bat       # Script Windows
├── 📋 requirements.txt       # Dependencias
├── 📝 env_example.txt        # Variables de entorno
├── 📖 README_SDF.md         # Este archivo
├── 📁 contexto/             # Documentos a analizar
└── 📁 vector_db/            # Base de datos vectorial
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` basado en `env_example.txt`:

```bash
# Configuración de Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:20b

# Configuración de Streamlit
STREAMLIT_PORT=8502
STREAMLIT_HOST=localhost

# Para acceso desde red local
# STREAMLIT_HOST=0.0.0.0
```

### Modelos Soportados

- `gpt-oss:20b` (recomendado)
- `llama2:7b`
- `mistral:7b`
- `codellama:7b`
- Cualquier modelo de Ollama

## 📚 Cómo Usar

### 1. Preparar Documentos
Coloca tus documentos en la carpeta `contexto/`:
- 📊 Excel (.xlsx, .xls)
- 📄 PDF (.pdf)
- 📋 CSV (.csv)
- 📝 Word (.docx)
- 📄 Texto (.txt, .md)

### 2. Hacer Preguntas
Ejemplos de preguntas:
- "¿Cuántos empleados hay en el archivo Excel?"
- "¿Qué políticas contiene el documento PDF?"
- "Analiza los datos de ventas del CSV"
- "¿Qué información hay sobre la empresa?"

### 3. Obtener Respuestas
SDF Assistant automáticamente:
- 🔍 Busca documentos relevantes usando palabras clave
- 📊 Analiza solo el contenido pertinente
- 💬 Genera respuestas precisas y contextualizadas
- 📈 Proporciona insights útiles

## 🔍 Búsqueda Dinámica de Contexto

### ¿Cómo Funciona?

1. **Extracción de Palabras Clave**: Analiza tu pregunta para identificar términos importantes
2. **Búsqueda Inteligente**: Busca documentos que contengan esas palabras clave
3. **Puntuación de Relevancia**: Asigna una puntuación a cada documento basada en la relevancia
4. **Selección Optimizada**: Usa solo los documentos más relevantes para generar la respuesta
5. **Contexto Dinámico**: Construye el contexto solo con la información necesaria

### Ventajas

- ⚡ **Más Rápido**: Procesa menos documentos
- 🎯 **Más Preciso**: Usa solo información relevante
- 💾 **Menos Memoria**: Reduce el uso de recursos
- 🔍 **Mejor Búsqueda**: Encuentra información específica más fácilmente

## 🔧 Solución de Problemas

### Ollama no está ejecutándose
```bash
ollama serve
```

### Modelo no encontrado
```bash
ollama pull gpt-oss:20b
```

### Puerto ocupado
Cambia `STREAMLIT_PORT` en `.env`:
```bash
STREAMLIT_PORT=8503
```

### Acceso desde red local
Cambia en `.env`:
```bash
STREAMLIT_HOST=0.0.0.0
```

### Verificar Sistema
```bash
python check_system_sdf.py
```

## 🛠️ Desarrollo

### Estructura del Código

- **`app_sdf.py`**: Interfaz de usuario con Streamlit
- **`sdf_assistant.py`**: Lógica principal con búsqueda dinámica
- **`document_processor.py`**: Procesamiento de documentos
- **`config.py`**: Configuración centralizada

### Agregar Nuevos Tipos de Documentos

1. Edita `config.py` - `SUPPORTED_EXTENSIONS`
2. Implementa el procesador en `document_processor.py`
3. Actualiza `requirements.txt` si es necesario

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección de [Solución de Problemas](#-solución-de-problemas)
2. Ejecuta: `python check_system_sdf.py`
3. Abre un [Issue](https://github.com/tu-usuario/Chatbot/issues)

## 🎉 Agradecimientos

- [Ollama](https://ollama.ai) por los modelos de IA local
- [Streamlit](https://streamlit.io) por la interfaz web
- [LangChain](https://langchain.com) por el framework de IA

---

**¡Disfruta usando SDF Assistant! 🚀**
