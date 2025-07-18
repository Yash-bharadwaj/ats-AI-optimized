#!/usr/bin/env python3
"""
Test script to verify all imports work correctly for Railway deployment
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports for Railway deployment...")
    
    try:
        # Test core imports
        print("✅ Testing core imports...")
        from app.main import app
        print("✅ app.main imported successfully")
        
        # Test API imports
        print("✅ Testing API imports...")
        from app.api.v1.api import api_router
        print("✅ app.api.v1.api imported successfully")
        
        # Test models imports
        print("✅ Testing models imports...")
        from app.models import (
            JobCreateRequest,
            JobResponse,
            JobListResponse,
            JobDescriptionParseRequest,
            JobDescriptionResponse,
            JobStatus,
            JobType,
            Priority
        )
        print("✅ app.models imported successfully")
        
        # Test services imports
        print("✅ Testing services imports...")
        from app.services.job_service import JobService
        from app.services.file_processors import FileProcessor
        from app.services.groq_service import GroqService
        from app.services.vector_service import VectorService
        print("✅ app.services imported successfully")
        
        # Test endpoints imports
        print("✅ Testing endpoints imports...")
        from app.api.v1.endpoints import resume, job_description, jobs, applicants
        print("✅ app.api.v1.endpoints imported successfully")
        
        print("🎉 All imports successful! Ready for Railway deployment.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 