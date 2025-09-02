#!/bin/bash
set -e

echo "🔎 Checking Postgres roles and databases..."

# Intentar entrar con usuario actual de macOS
psql -U $(whoami) -d postgres -c "\du"
psql -U $(whoami) -d postgres -c "\l"
