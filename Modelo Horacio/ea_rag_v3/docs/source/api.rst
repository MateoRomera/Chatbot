API REST
========

Formato estándar
----------------

- Respuesta exitosa:

.. code-block:: json

   { "success": true, "data": {...} }

- Respuesta con error:

.. code-block:: json

   { "success": false, "error": "mensaje" }

Endpoints
---------

**/api/health**
   Verifica estado del backend.

**/api/ask**
   Procesa consultas en lenguaje natural.

**/api/structured_query**
   Ejecuta búsqueda filtrada en Postgres.

Ejemplos
--------

.. code-block:: bash

   curl http://127.0.0.1:8000/api/health
   curl "http://127.0.0.1:8000/api/ask?query=hola"
   curl "http://127.0.0.1:8000/api/structured_query?fuerza=Ejército&provincia=Mendoza"

