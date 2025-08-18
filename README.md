# 🤖 NachoGPT - Asistente IA Avanzado

Un asistente de inteligencia artificial local que utiliza Ollama para procesar y analizar documentos de manera inteligente.

## ✨ Características

- 🔍 **Análisis Inteligente**: Procesa documentos Excel, PDF, CSV, Word y más
- 🧠 **IA Local**: Utiliza modelos de Ollama sin necesidad de conexión a internet
- 📊 **Contexto Dinámico**: Analiza automáticamente los documentos relevantes
- 🎯 **Búsqueda Inteligente**: Encuentra información específica en tus documentos
- 💬 **Interfaz Web**: Interfaz moderna y fácil de usar con Streamlit
- 🔧 **Configurable**: Personalizable para diferentes modelos y configuraciones

## 🚀 Instalación Rápida

### Requisitos Previos

1. **Python 3.8 o superior**
2. **Ollama** instalado y ejecutándose
3. **Git** (para clonar el repositorio)

### Pasos de Instalación

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/NachoGPT.git
cd NachoGPT
```

#### 2. Instalación Automática (Recomendado)
```bash
python setup_nachogpt.py
```

#### 3. Instalación Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar modelo de IA
ollama pull gpt-oss:20b

# Crear carpeta de contexto
mkdir contexto
```

## 🎯 Uso

### Ejecutar NachoGPT

#### Opción 1: Script Python
```bash
python run_nachogpt.py
```

#### Opción 2: Script Batch (Windows)
```bash
iniciar_nachogpt.bat
```

#### Opción 3: Directo con Streamlit
```bash
streamlit run app_nachogpt.py
```

### Acceder a la Aplicación

1. Abre tu navegador
2. Ve a: `http://localhost:8501`
3. ¡Listo para usar!

## 📁 Estructura del Proyecto

```
NachoGPT/
├── 📄 app_nachogpt.py          # Aplicación principal
├── 🤖 simple_ai_assistant.py   # Lógica del asistente
├── 📊 document_processor.py    # Procesador de documentos
├── ⚙️ config.py               # Configuración
├── 🚀 run_nachogpt.py         # Script de ejecución
├── 📦 setup_nachogpt.py       # Instalador automático
├── 🖥️ iniciar_nachogpt.bat    # Script Windows
├── 📋 requirements.txt        # Dependencias
├── 📝 env_example.txt         # Variables de entorno
├── 📖 README.md              # Este archivo
├── 📁 contexto/              # Documentos a analizar
└── 📁 vector_db/             # Base de datos vectorial
```

## ⚙️ Configuración

### Variables de Entorno

Crea un archivo `.env` basado en `env_example.txt`:

```bash
# Configuración de Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:20b

# Configuración de Streamlit
STREAMLIT_PORT=8501
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
NachoGPT automáticamente:
- 🔍 Busca documentos relevantes
- 📊 Analiza el contenido
- 💬 Genera respuestas precisas
- 📈 Proporciona insights útiles

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
STREAMLIT_PORT=8502
```

### Acceso desde red local
Cambia en `.env`:
```bash
STREAMLIT_HOST=0.0.0.0
```

## 🛠️ Desarrollo

### Estructura del Código

- **`app_nachogpt.py`**: Interfaz de usuario con Streamlit
- **`simple_ai_assistant.py`**: Lógica principal del asistente
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
2. Abre un [Issue](https://github.com/tu-usuario/NachoGPT/issues)
3. Consulta la [documentación](https://github.com/tu-usuario/NachoGPT/wiki)

## 🎉 Agradecimientos

- [Ollama](https://ollama.ai) por los modelos de IA local
- [Streamlit](https://streamlit.io) por la interfaz web
- [LangChain](https://langchain.com) por el framework de IA

---

**¡Disfruta usando NachoGPT! 🚀**