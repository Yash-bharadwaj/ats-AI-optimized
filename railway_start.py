#!/usr/bin/env python3
"""
Railway startup script for AI Recruitment Platform
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

def main():
    """Start the Railway server"""
    # Get port from environment variable with proper fallback
    try:
        port = int(os.environ.get("PORT", 8000))
    except (ValueError, TypeError):
        port = 8000
    
    print(f"🚀 Starting AI Recruitment Platform on Railway")
    print(f"📡 Port: {port}")
    print(f"🌐 Host: 0.0.0.0")
    print(f"🔧 Environment: {os.environ.get('RAILWAY_ENVIRONMENT', 'production')}")
    print("=" * 60)
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=port,
            workers=1,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 