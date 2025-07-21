#!/bin/bash

# Railway startup script with proper PORT handling

# Get the port from environment variable or default to 8000
PORT=${PORT:-8000}

echo "🚀 Starting AI Recruitment Platform on Railway"
echo "📡 Port: $PORT"
echo "🌐 Host: 0.0.0.0"
echo "🔧 Environment: ${RAILWAY_ENVIRONMENT:-production}"
echo "============================================================"

# Start the FastAPI application
exec python3 railway_start.py 