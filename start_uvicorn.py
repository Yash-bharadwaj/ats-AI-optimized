#!/usr/bin/env python3
"""
Direct uvicorn startup for Railway
"""

import uvicorn
import os

if __name__ == "__main__":
    # Get port from environment variable
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting on port {port}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        workers=1
    ) 