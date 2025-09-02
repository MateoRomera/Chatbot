#!/bin/bash
set -e

echo "🔎 Checking status of backend and frontend..."

BACKEND_PID=$(pgrep -f "uvicorn" || true)
FRONTEND_PID=$(pgrep -f "http.server" || true)

if [ -n "$BACKEND_PID" ]; then
    echo "✅ Backend (uvicorn) is running with PID(s): $BACKEND_PID"
else
    echo "❌ Backend (uvicorn) is NOT running"
fi

if [ -n "$FRONTEND_PID" ]; then
    echo "✅ Frontend (http.server) is running with PID(s): $FRONTEND_PID"
else
    echo "❌ Frontend (http.server) is NOT running"
fi
