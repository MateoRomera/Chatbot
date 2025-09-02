# EA RAG v3 Chatbot - Personal Militar Argentino

Este es un chatbot que lee datos del personal militar argentino y permite hacer consultas en lenguaje natural.

## Características

- **Chat IA**: Consultas en lenguaje natural sobre personal militar
- **Query Estructurada**: Búsquedas filtradas por fuerza, provincia y especialidad
- **Datos**: Utiliza archivos SQLite y CSV con información del personal
- **Interfaz Web**: Interfaz moderna y responsive

## Instalación y Uso

### Opción 1: Script Automático (Recomendado)

1. **Ejecutar el script de inicio:**
   ```powershell
   .\start_chatbot.ps1
   ```
   
   O si prefieres el archivo .bat:
   ```cmd
   start_chatbot.bat
   ```

2. **El script automáticamente:**
   - Activa el entorno virtual
   - Inicia el servidor backend (puerto 8000)
   - Inicia el servidor frontend (puerto 8080)
   - Abre el navegador en http://localhost:8080

### Opción 2: Manual

1. **Activar entorno virtual:**
   ```powershell
   venv\Scripts\Activate.ps1
   ```

2. **Instalar dependencias (si no están instaladas):**
   ```powershell
   pip install fastapi uvicorn pandas openpyxl python-dotenv
   ```

3. **Iniciar backend:**
   ```powershell
   python backend\app_sqlite.py
   ```

4. **En otra terminal, iniciar frontend:**
   ```powershell
   cd frontend
   python -m http.server 8080
   ```

5. **Abrir navegador:**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:8000

## Uso del Chatbot

### Chat IA
Puedes hacer preguntas como:
- "Muéstrame personal del ejército"
- "Busca médicos en Buenos Aires"
- "Personal de la fuerza aérea en Córdoba"
- "Ingenieros de la armada"

### Query Estructurada
Usa los filtros para buscar:
- **Fuerza**: Ejército, Armada, Fuerza Aérea
- **Provincia**: Buenos Aires, Córdoba, Mendoza, etc.
- **Especialidad**: Ingeniero, Médico, Infantería, etc.

## Estructura del Proyecto

```
ea_rag_v3/
├── backend/
│   ├── app_sqlite.py      # Servidor FastAPI (SQLite)
│   └── data_loader.py     # Cargador de datos
├── frontend/
│   ├── index.html         # Interfaz web
│   └── app.js            # JavaScript del frontend
├── data/                  # Archivos de datos
│   ├── personal_*.sqlite  # Bases de datos SQLite
│   └── personal_*.csv     # Archivos CSV
├── venv/                  # Entorno virtual Python
├── start_chatbot.ps1      # Script de inicio PowerShell
└── start_chatbot.bat      # Script de inicio Batch
```

## Datos Disponibles

El chatbot incluye datos de personal militar con información como:
- Nombre completo
- Fuerza (Ejército, Armada, Fuerza Aérea)
- Provincia
- Especialidad
- Grado o rango
- Información de contacto

## API Endpoints

- `GET /api/health` - Estado del servidor
- `GET /api/ask?query=texto` - Consulta en lenguaje natural
- `GET /api/structured_query?fuerza=X&provincia=Y&especialidad=Z` - Query estructurada

## Solución de Problemas

### Error de conexión al backend
- Verifica que el servidor backend esté ejecutándose en el puerto 8000
- Revisa los logs en `logs/backend.log`

### Error de módulos Python
- Asegúrate de que el entorno virtual esté activado
- Reinstala las dependencias: `pip install -r requirements.txt`

### Puerto ocupado
- Cambia los puertos en los archivos de configuración
- O termina los procesos que usen los puertos 8000/8080

## Tecnologías Utilizadas

- **Backend**: FastAPI, Python, SQLite, Pandas
- **Frontend**: HTML5, CSS3, JavaScript
- **Datos**: SQLite, CSV
- **Servidor**: Uvicorn, Python HTTP Server
