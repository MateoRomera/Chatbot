# Solución: Recarga Automática de Datos en el Chatbot

## Problema Identificado

El chatbot no leía nuevos documentos cuando se agregaban a la carpeta `data`. Esto ocurría porque:

1. **Carga única**: Los archivos de datos se cargaban solo una vez al inicializar el sistema
2. **Sin mecanismo de recarga**: No había forma de actualizar la lista de archivos sin reiniciar el servidor
3. **Limitación de formatos**: Solo manejaba archivos SQLite y CSV, no JSON ni XLSX

## Solución Implementada

### 1. Nuevos Endpoints de API

Se agregaron dos nuevos endpoints al backend (`backend/app_sqlite.py`):

#### `POST /api/reload_data`
- **Función**: Recarga todos los archivos de datos desde el disco
- **Respuesta**: Lista de archivos detectados y mensaje de confirmación
- **Uso**: Se llama cuando se agregan nuevos documentos

#### `GET /api/data_files`
- **Función**: Muestra los archivos de datos actualmente cargados
- **Respuesta**: Lista detallada con nombre, tipo y tamaño de cada archivo
- **Uso**: Para verificar qué archivos están disponibles

### 2. Mejoras en el Cargador de Datos

#### Soporte para más formatos:
- ✅ **SQLite** (`.sqlite`, `.db`)
- ✅ **CSV** (`.csv`)
- ✅ **JSON** (`.json`)
- ✅ **Excel** (`.xlsx`, `.xls`)

#### Método de recarga dinámica:
```python
def reload_data(self):
    """Reload data files from disk"""
    self.load_data_files()
    logging.info("Data files reloaded successfully")
    return {"message": f"Reloaded {len(self.data_files)} data files", 
            "files": [f.name for f in self.data_files]}
```

### 3. Interfaz de Usuario Mejorada

Se agregó una nueva sección "Administración de Datos" al frontend con:

- **🔄 Botón "Recargar Datos"**: Ejecuta la recarga automática
- **📁 Botón "Ver Archivos"**: Muestra los archivos cargados
- **Feedback visual**: Indicadores de estado y resultados

### 4. Scripts de Prueba

#### `test_reload.py`
- Prueba la funcionalidad básica de recarga
- Verifica que los endpoints funcionen correctamente

#### `add_test_document.py`
- Crea un documento de prueba
- Verifica que se detecte automáticamente
- Prueba consultas con el nuevo documento

## Cómo Usar la Solución

### 1. Agregar un Nuevo Documento

1. Coloca tu archivo en la carpeta `data/`
2. Formatos soportados: `.csv`, `.json`, `.xlsx`, `.sqlite`
3. El archivo debe tener columnas como: `Nombre completo`, `Fuerza`, `Provincia`, `Especialidad`

### 2. Recargar los Datos

#### Opción A: Desde la interfaz web
1. Abre http://localhost:8080
2. Ve a la sección "Administración de Datos"
3. Haz clic en "🔄 Recargar Datos"
4. Verifica que tu archivo aparezca en la lista

#### Opción B: Desde la API
```bash
curl -X POST http://localhost:8000/api/reload_data
```

#### Opción C: Ver archivos cargados
```bash
curl http://localhost:8000/api/data_files
```

### 3. Verificar que Funciona

1. Haz una consulta en el chat con datos de tu nuevo documento
2. Usa la query estructurada con filtros que coincidan con tu documento
3. Verifica que los resultados incluyan datos del nuevo archivo

## Estructura de Datos Esperada

### Para archivos CSV/Excel:
```csv
Nombre completo,Fuerza,Provincia,Especialidad,Grado o Rango
Juan Pérez,Ejército,Buenos Aires,Ingeniero,Teniente
María García,Armada,Córdoba,Médico,Capitán
```

### Para archivos JSON:
```json
[
  {
    "Nombre completo": "Juan Pérez",
    "Fuerza": "Ejército",
    "Provincia": "Buenos Aires",
    "Especialidad": "Ingeniero",
    "Grado o Rango": "Teniente"
  }
]
```

### Para archivos SQLite:
```sql
CREATE TABLE personal (
    id INTEGER PRIMARY KEY,
    nombre_completo TEXT,
    fuerza TEXT,
    provincia TEXT,
    especialidad TEXT,
    grado_o_rango TEXT
);
```

## Ventajas de la Solución

1. **✅ Sin reinicio**: No necesitas reiniciar el servidor
2. **✅ Tiempo real**: Los nuevos documentos se detectan inmediatamente
3. **✅ Múltiples formatos**: Soporta CSV, JSON, Excel y SQLite
4. **✅ Interfaz amigable**: Botones en la web para recargar
5. **✅ Logging**: Registra todas las operaciones para debugging
6. **✅ Robustez**: Maneja errores graciosamente

## Troubleshooting

### Si un archivo no se detecta:
1. Verifica que esté en la carpeta `data/`
2. Asegúrate de que tenga una extensión válida (`.csv`, `.json`, `.xlsx`, `.sqlite`)
3. Revisa los logs en `logs/backend.log`
4. Usa el botón "📁 Ver Archivos" para verificar

### Si hay errores de formato:
1. Verifica que las columnas tengan nombres correctos
2. Asegúrate de que el archivo no esté corrupto
3. Revisa la codificación (UTF-8 recomendado)

### Si el servidor no responde:
1. Verifica que esté ejecutándose en el puerto 8000
2. Revisa los logs para errores
3. Reinicia el servidor si es necesario

## Próximas Mejoras Posibles

1. **Monitoreo automático**: Detectar cambios en la carpeta automáticamente
2. **Validación de datos**: Verificar formato y estructura de archivos
3. **Backup automático**: Crear copias de seguridad antes de recargar
4. **Notificaciones**: Alertas cuando se detecten nuevos archivos
5. **Filtros avanzados**: Búsqueda por fecha de modificación, tamaño, etc.
