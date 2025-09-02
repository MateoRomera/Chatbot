#!/bin/bash
set -e

echo "🛑 Stopping backend and frontend..."

# Kill backend (uvicorn) and frontend (http.server)
pkill -f "uvicorn" || true
pkill -f "http.server" || true

echo "✅ All services stopped."
