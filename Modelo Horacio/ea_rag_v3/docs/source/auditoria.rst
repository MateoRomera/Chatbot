Auditoría y trazabilidad
========================

El sistema mantiene un registro completo:

- **Logs de backend** (`logs/backend.log`)
  - Inicio de backend
  - Consultas ASK y STRUCTURED
  - Errores de conexión o SQL

Ejemplo
-------

.. code-block:: text

   2025-08-19 [STRUCTURED] filtros=['Ejército','Mendoza'] → 5 resultados
   2025-08-19 [ASK] query='médicos del ejército en Córdoba' → response='Encontré 1 resultado(s): Valentina Sánchez'

Seguridad
---------

- Configuración sensible en `.env`.
- Sin credenciales hardcodeadas.
- Auditoría legible para ingeniería.

