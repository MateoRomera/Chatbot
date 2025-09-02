Flujo funcional
===============

1. El usuario interactúa con el **frontend**.
2. El frontend envía request AJAX al **backend FastAPI**.
3. El backend procesa:
   - Si es chat → heurística de filtros.
   - Si es estructurado → SQL directo.
4. PostgreSQL responde.
5. El backend devuelve JSON uniforme.
6. El frontend lo renderiza en chat o tabla.

