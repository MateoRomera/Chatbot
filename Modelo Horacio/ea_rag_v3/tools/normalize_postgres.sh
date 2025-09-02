#!/bin/bash
# tools/normalize_postgres.sh
# Normaliza columnas de la tabla 'personal' en PostgreSQL

DB_NAME="ea_rag"
DB_USER="horacio"
PSQL_BIN="/usr/local/opt/postgresql@15/bin/psql"

echo "🔧 Normalizando columnas de la tabla 'personal' en PostgreSQL..."

$PSQL_BIN -d $DB_NAME -U $DB_USER <<SQL
-- Renombrar columnas a snake_case sin tildes
ALTER TABLE personal RENAME COLUMN IF EXISTS "Nombre completo" TO nombre_completo;
ALTER TABLE personal RENAME COLUMN IF EXISTS "Formación universitaria" TO formacion;

-- Verificar estructura final
\d personal;
SQL

echo "✅ Normalización completada."
