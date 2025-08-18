# 🤖 SDF Assistant Enterprise - Document Intelligence Platform

**Versión 2.0 - Plataforma de Inteligencia Documental Empresarial**

SDF Assistant Enterprise es una plataforma avanzada de análisis de documentos que combina inteligencia artificial local con capacidades empresariales robustas, monitoreo en tiempo real y herramientas de administración integrales.

## ✨ Características Enterprise

### 🧠 **Inteligencia Avanzada**
- **Búsqueda Dinámica de Contexto**: Encuentra automáticamente documentos relevantes para cada consulta
- **Análisis Semántico**: Procesamiento inteligente con extracción de palabras clave mejorada
- **Modelos IA Locales**: Utiliza Ollama para procesamiento sin dependencias externas
- **Respuestas Contextualizadas**: Genera respuestas precisas basadas en documentos específicos

### 📊 **Monitoreo Enterprise**
- **Métricas en Tiempo Real**: CPU, memoria, disco, conexiones de red
- **Análisis de Rendimiento**: Tiempo de respuesta, tasa de éxito, confianza
- **Alertas Automáticas**: Notificaciones de problemas del sistema
- **Logs Estructurados**: Registro detallado de todas las operaciones

### 🔧 **Panel de Administración**
- **Dashboard Interactivo**: Métricas visuales con gráficos en tiempo real
- **Gestión de Documentos**: Carga, análisis y organización de archivos
- **Configuración del Sistema**: Ajuste de parámetros sin reinicio
- **Backup y Restauración**: Copias de seguridad automáticas

### 🛡️ **Seguridad y Robustez**
- **Procesamiento Local**: Todos los datos permanecen en tu infraestructura
- **Aislamiento de Documentos**: Procesamiento seguro sin exposición externa
- **Logging Asíncrono**: No bloquea operaciones principales
- **Recuperación de Errores**: Manejo robusto de fallos del sistema

## 🚀 Instalación Enterprise

### Requisitos del Sistema

- **Python 3.8+**
- **Ollama** (versión estable)
- **8GB+ RAM** (recomendado)
- **2GB+ espacio libre**
- **Windows 10/11** o **Linux/macOS**

### Instalación Automática

#### Opción 1: Script Enterprise (Recomendado)
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/Chatbot.git
cd Chatbot/SDF_Assistant

# Instalación enterprise automática
python run_enterprise.py
```

#### Opción 2: Script Batch (Windows)
```bash
# Ejecutar script enterprise
iniciar_enterprise.bat
```

#### Opción 3: Instalación Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Instalar modelo de IA
ollama pull gpt-oss:20b

# Crear directorios enterprise
mkdir logs backups exports temp contexto
```

## 🎯 Uso Enterprise

### Inicio de la Plataforma

Al ejecutar `run_enterprise.py`, tendrás acceso a:

1. **🚀 Aplicación Principal**: Chat interactivo con análisis de documentos
2. **🔧 Panel de Administración**: Gestión completa del sistema
3. **📊 Solo Monitoreo**: Dashboard de métricas en tiempo real

### URLs de Acceso

- **Aplicación Principal**: `http://localhost:8502`
- **Panel de Administración**: `http://localhost:8503`
- **Monitoreo**: Integrado en el panel de administración

## 📊 Panel de Administración

### System Overview
- **Health Score**: Puntuación general del sistema (0-100%)
- **CPU Usage**: Uso de procesador en tiempo real
- **Memory Usage**: Consumo de memoria del sistema
- **Queries/Min**: Consultas procesadas por minuto
- **Ollama Status**: Estado del servicio de IA
- **Document Status**: Información de documentos cargados

### Performance Analytics
- **Response Time Trend**: Evolución del tiempo de respuesta
- **Success Rate**: Tasa de éxito de las consultas
- **Confidence Scores**: Puntuaciones de confianza promedio
- **Query Statistics**: Estadísticas detalladas de consultas

### System Monitoring
- **CPU & Memory Usage**: Gráficos de recursos del sistema
- **Disk Usage**: Uso de almacenamiento
- **System Alerts**: Alertas automáticas de problemas
- **Network Connections**: Conexiones activas

### Document Management
- **Document Statistics**: Estadísticas de documentos cargados
- **File Type Distribution**: Distribución por tipos de archivo
- **Document List**: Lista detallada de documentos
- **Document Actions**: Recargar, resumir, exportar

### System Configuration
- **Current Configuration**: Configuración actual del sistema
- **Model Selection**: Cambio de modelos de IA
- **Performance Tuning**: Ajuste de parámetros
- **System Logs**: Visualización de logs del sistema

### Backup & Restore
- **Backup Operations**: Creación de copias de seguridad
- **Restore Operations**: Restauración de backups
- **Export Analytics**: Exportación de datos de análisis
- **Export Conversations**: Exportación de conversaciones

## ⚙️ Configuración Enterprise

### Variables de Entorno

Crea un archivo `.env` con las siguientes configuraciones:

```bash
# Configuración de Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gpt-oss:20b

# Configuración de Streamlit
STREAMLIT_PORT=8502
STREAMLIT_HOST=localhost

# Configuración de Rendimiento
MAX_TOKENS=8192
TEMPERATURE=0.7
MAX_CONTEXT_LENGTH=8000
MAX_WORKERS=4

# Configuración Enterprise
ENABLE_MONITORING=true
MONITORING_INTERVAL=30
LOG_LEVEL=INFO
```

### Modelos Soportados

- `gpt-oss:20b` (recomendado para enterprise)
- `llama2:7b`
- `mistral:7b`
- `codellama:7b`
- Cualquier modelo de Ollama

## 📁 Estructura del Proyecto Enterprise

```
SDF_Assistant/
├── 📄 app_sdf.py                 # Aplicación principal enterprise
├── 🔧 admin_panel.py             # Panel de administración
├── 📊 enterprise_monitor.py      # Sistema de monitoreo
├── 🤖 sdf_assistant.py           # Lógica del asistente enterprise
├── 📊 document_processor.py      # Procesador de documentos
├── ⚙️ config.py                 # Configuración enterprise
├── 🚀 run_enterprise.py         # Lanzador enterprise
├── 🖥️ iniciar_enterprise.bat   # Script Windows enterprise
├── 📦 requirements.txt           # Dependencias enterprise
├── 📝 env_example.txt           # Variables de entorno
├── 📖 README_ENTERPRISE.md      # Esta documentación
├── 📁 logs/                     # Logs del sistema
├── 📁 backups/                  # Copias de seguridad
├── 📁 exports/                  # Exportaciones
├── 📁 temp/                     # Archivos temporales
├── 📁 contexto/                 # Documentos a analizar
└── 📁 vector_db/                # Base de datos vectorial
```

## 🔍 Funcionalidades Avanzadas

### Búsqueda Dinámica de Contexto

1. **Extracción de Palabras Clave**: Análisis semántico de consultas
2. **Búsqueda Inteligente**: Identificación de documentos relevantes
3. **Puntuación de Relevancia**: Algoritmo de scoring avanzado
4. **Selección Optimizada**: Uso de solo documentos pertinentes
5. **Contexto Dinámico**: Construcción inteligente del contexto

### Monitoreo en Tiempo Real

- **Métricas del Sistema**: CPU, memoria, disco, red
- **Métricas de Rendimiento**: Tiempo de respuesta, éxito, confianza
- **Alertas Automáticas**: Notificaciones de problemas
- **Logs Estructurados**: Registro detallado de operaciones

### Herramientas de Administración

- **Dashboard Interactivo**: Métricas visuales en tiempo real
- **Gestión de Documentos**: Carga y organización de archivos
- **Configuración Dinámica**: Ajustes sin reinicio
- **Backup Automático**: Copias de seguridad programadas

## 🛠️ Desarrollo Enterprise

### Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Monitoring    │
│   (Streamlit)   │◄──►│   (SDF Core)    │◄──►│   (Enterprise)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Admin Panel   │    │   Document      │    │   System        │
│   (Management)  │    │   Processor     │    │   Monitor       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Componentes Principales

- **`SDFAssistant`**: Lógica principal con búsqueda dinámica
- **`EnterpriseMonitor`**: Sistema de monitoreo y logging
- **`DocumentProcessor`**: Procesamiento de múltiples formatos
- **`AdminPanel`**: Interfaz de administración

### Extensibilidad

El sistema está diseñado para ser extensible:

1. **Nuevos Tipos de Documentos**: Agregar procesadores en `document_processor.py`
2. **Métricas Personalizadas**: Extender `enterprise_monitor.py`
3. **Funcionalidades de Admin**: Agregar secciones en `admin_panel.py`
4. **Modelos de IA**: Configurar nuevos modelos en `config.py`

## 🔧 Solución de Problemas Enterprise

### Problemas Comunes

#### Ollama no responde
```bash
# Verificar servicio
ollama serve

# Verificar modelo
ollama list
```

#### Puerto ocupado
```bash
# Cambiar puerto en .env
STREAMLIT_PORT=8503
```

#### Memoria insuficiente
```bash
# Reducir workers en .env
MAX_WORKERS=2
MAX_CONTEXT_LENGTH=4000
```

#### Logs de error
```bash
# Verificar logs
tail -f logs/sdf_errors.log
```

### Verificación del Sistema

```bash
# Verificación completa
python check_system_sdf.py

# Verificación enterprise
python run_enterprise.py
```

## 📈 Métricas y Analytics

### Health Score

El sistema calcula un Health Score basado en:

- **CPU Usage**: < 80% = +25 puntos
- **Memory Usage**: < 85% = +25 puntos
- **Disk Usage**: < 90% = +20 puntos
- **Ollama Status**: Online = +30 puntos

### Performance Metrics

- **Response Time**: Tiempo promedio de respuesta
- **Success Rate**: Tasa de éxito de consultas
- **Confidence Score**: Puntuación de confianza promedio
- **Documents Used**: Promedio de documentos utilizados

### System Alerts

El sistema genera alertas automáticas para:

- CPU > 80%
- Memory > 85%
- Disk > 90%
- Ollama offline
- Error rate > 10%

## 🔒 Seguridad Enterprise

### Características de Seguridad

- **Procesamiento Local**: Sin dependencias externas
- **Aislamiento de Datos**: Documentos procesados localmente
- **Logs Seguros**: Sin información sensible en logs
- **Configuración Protegida**: Variables de entorno para credenciales

### Mejores Prácticas

1. **Mantener Ollama Local**: No exponer a internet
2. **Actualizar Dependencias**: Mantener paquetes actualizados
3. **Monitorear Logs**: Revisar logs regularmente
4. **Backup Regular**: Crear copias de seguridad frecuentes

## 📞 Soporte Enterprise

### Canales de Soporte

1. **Documentación**: Esta guía y README_SDF.md
2. **Logs del Sistema**: `logs/sdf_main.log`
3. **Verificación**: `python check_system_sdf.py`
4. **Issues**: GitHub repository

### Información de Diagnóstico

Para reportar problemas, incluye:

- Versión de Python
- Versión de Ollama
- Modelo utilizado
- Logs de error
- Configuración del sistema

## 🎉 Agradecimientos Enterprise

- [Ollama](https://ollama.ai) por los modelos de IA local
- [Streamlit](https://streamlit.io) por la interfaz web
- [LangChain](https://langchain.com) por el framework de IA
- [Plotly](https://plotly.com) por las visualizaciones
- [psutil](https://psutil.readthedocs.io) por el monitoreo del sistema

---

**SDF Assistant Enterprise - Document Intelligence Platform v2.0**

*Transformando el análisis de documentos con inteligencia artificial empresarial* 🚀
