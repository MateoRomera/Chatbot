#!/bin/bash
set -e

# Activate venv
source .venv/bin/activate

# Kill old uvicorn (backend) and http.server (frontend) if running
echo "🔎 Stopping old processes..."
pkill -f "uvicorn" || true
pkill -f "http.server" || true

# Start backend
echo "🚀 Starting backend..."
nohup ./run_backend.sh > backend.log 2>&1 &

# Start frontend
echo "🚀 Starting frontend..."
nohup ./run_frontend.sh > frontend.log 2>&1 &

sleep 2
echo "✅ All services restarted."
echo "   Backend: http://127.0.0.1:8000"
echo "   Frontend: http://127.0.0.1:8080"
