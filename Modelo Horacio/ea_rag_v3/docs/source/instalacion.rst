Instalación y despliegue
========================

Requisitos
----------

- Python 3.10+
- PostgreSQL 14+
- 4 GB RAM mínimo
- 2 núcleos CPU

Pasos
-----

1. Clonar repositorio:

   .. code-block:: bash

      git clone <url_repo>
      cd ea_rag_v3

2. Crear entorno virtual:

   .. code-block:: bash

      python3 -m venv .venv
      source .venv/bin/activate

3. Instalar dependencias:

   .. code-block:: bash

      pip install -r requirements.txt

4. Configurar `.env`:

   .. code-block:: bash

      POSTGRES_CONN=dbname=ea_rag user=Horacio host=localhost

5. Levantar el sistema:

   .. code-block:: bash

      make restart

