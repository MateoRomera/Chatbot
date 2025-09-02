Arquitectura del sistema
========================

Visión general
--------------

El sistema está organizado en 4 capas principales:

1. **Frontend** (HTML/JS/CSS) – interfaz responsiva.  
2. **Backend** (FastAPI) – API REST.  
3. **Base de datos** (Postgres) – tabla `personal`.  
4. **Automatización** (Makefile) – orquestación.

Diagrama lógico
---------------

.. mermaid::

   graph TD
     U[Usuario]
     F[Frontend Web]
     B[Backend FastAPI]
     D[(Postgres)]

     U --> F
     F --> B
     B --> D
     D --> B
     B --> F

Patrones aplicados
------------------

- API RESTful  
- Separación de capas (MVC simplificado)  
- Configuración en `.env` (12-factor app)  

