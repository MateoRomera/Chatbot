# Instrucciones Corregidas - EA RAG v3 Chatbot

## Problema Solucionado

El problema que tenías era que los scripts se ejecutaban desde el directorio `C:\Windows\System32` en lugar del directorio del proyecto, causando errores de "archivo no encontrado".

## Solución Implementada

He corregido los scripts de inicio para que funcionen correctamente desde cualquier ubicación:

### ✅ Scripts Corregidos

1. **`start_simple.bat`** - Script Windows mejorado
2. **`start_simple.ps1`** - Script PowerShell mejorado
3. **`check_setup.py`** - Script de verificación

## Cómo Usar (Paso a Paso)

### 1. Verificar Configuración

Primero, ejecuta el script de verificación:

```bash
python check_setup.py
```

Este script te dirá si todo está configurado correctamente.

### 2. Iniciar el Chatbot

#### Opción A: Script Simple (Recomendado)
```bash
# Windows
start_simple.bat

# PowerShell
.\start_simple.ps1
```

#### Opción B: Manual
```bash
# 1. Activar entorno virtual
venv\Scripts\activate.bat

# 2. Iniciar backend
python backend\app_sqlite.py

# 3. En otra terminal, iniciar frontend
cd frontend
python -m http.server 8080
```

### 3. Verificar que Funciona

1. Abre http://localhost:8080
2. Ve a la sección "Administración de Datos"
3. Haz clic en "📁 Ver Archivos" para ver los archivos cargados
4. Haz clic en "🔄 Recargar Datos" para probar la funcionalidad

## Características de los Scripts Corregidos

### ✅ `start_simple.bat`
- Detecta automáticamente el directorio del proyecto
- Verifica que todos los archivos necesarios existan
- Instala dependencias automáticamente si faltan
- Maneja errores graciosamente
- Proporciona mensajes informativos

### ✅ `start_simple.ps1`
- Funcionalidad similar al .bat pero para PowerShell
- Colores en la consola para mejor legibilidad
- Manejo robusto de errores
- Verificaciones automáticas

### ✅ `check_setup.py`
- Verifica Python y su versión
- Comprueba que estés en el directorio correcto
- Verifica el entorno virtual
- Comprueba dependencias instaladas
- Verifica archivos de datos
- Prueba el backend

## Troubleshooting

### Si el script no funciona:

1. **Ejecuta la verificación:**
   ```bash
   python check_setup.py
   ```

2. **Verifica que estés en el directorio correcto:**
   - Debes estar en la carpeta raíz del proyecto
   - Debe contener las carpetas `backend`, `frontend`, `data`, `venv`

3. **Si falta el entorno virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

4. **Si faltan dependencias:**
   ```bash
   pip install fastapi uvicorn pandas openpyxl python-dotenv
   ```

### Errores Comunes y Soluciones

| Error | Solución |
|-------|----------|
| `No such file or directory` | Ejecuta desde el directorio raíz del proyecto |
| `ModuleNotFoundError` | Activa el entorno virtual e instala dependencias |
| `venv not found` | Crea el entorno virtual: `python -m venv venv` |
| `Port already in use` | Cierra otros procesos en puertos 8000/8080 |

## Funcionalidad de Recarga de Datos

Una vez que el chatbot esté funcionando:

1. **Agregar nuevo documento:**
   - Coloca tu archivo en la carpeta `data/`
   - Formatos soportados: `.csv`, `.json`, `.xlsx`, `.sqlite`

2. **Recargar datos:**
   - Ve a http://localhost:8080
   - Sección "Administración de Datos"
   - Haz clic en "🔄 Recargar Datos"

3. **Verificar:**
   - Haz clic en "📁 Ver Archivos"
   - Tu nuevo archivo debe aparecer en la lista

## Scripts de Prueba

```bash
# Probar funcionalidad básica
python test_reload.py

# Probar con documento nuevo
python add_test_document.py
```

## Estructura del Proyecto

```
ea_rag_v3/
├── backend/
│   └── app_sqlite.py      # Servidor principal
├── frontend/
│   └── index.html         # Interfaz web
├── data/                  # Archivos de datos
├── venv/                  # Entorno virtual
├── start_simple.bat       # Script Windows
├── start_simple.ps1       # Script PowerShell
├── check_setup.py         # Verificación
└── test_reload.py         # Pruebas
```

## Resumen

Los scripts corregidos solucionan el problema de rutas y proporcionan:

- ✅ **Detección automática del directorio del proyecto**
- ✅ **Verificaciones de configuración**
- ✅ **Instalación automática de dependencias**
- ✅ **Manejo robusto de errores**
- ✅ **Mensajes informativos claros**

¡Ahora el chatbot debería funcionar correctamente sin problemas de rutas!
