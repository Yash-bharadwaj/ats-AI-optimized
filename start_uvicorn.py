#!/usr/bin/env python3
"""
Simple startup script for Railway deployment
"""

import os
import uvicorn

def main():
    """Start the FastAPI application"""
    try:
        # Get port from environment variable
        port = int(os.environ.get("PORT", 8000))
        print(f"Starting AI Recruitment Platform on port {port}")
        
        # Start uvicorn server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            workers=1,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"Error starting application: {e}")
        raise

if __name__ == "__main__":
    main() 