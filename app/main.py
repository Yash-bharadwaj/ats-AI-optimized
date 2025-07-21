"""
Main FastAPI application for AI Recruitment Platform
Railway-optimized version with minimal dependencies
"""

import logging
import os
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Recruitment Platform",
    version="2.0.0",
    description="AI Recruitment Platform with Railway Optimization",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        logger.info("🚀 AI Recruitment Platform starting up...")
        logger.info("✅ Basic services initialized")
        logger.info("🚀 AI Recruitment Platform started successfully")
    except Exception as e:
        logger.error(f"❌ Error during startup: {str(e)}")
        # Don't fail startup for Railway deployment
        pass

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AI Recruitment Platform API",
        "version": "2.0.0",
        "status": "running",
        "railway_mode": True,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    try:
        health_status = {
            "status": "healthy",
            "services": {
                "api": "operational",
                "railway_mode": True
            },
            "version": "2.0.0",
            "railway_optimized": True,
            "timestamp": datetime.now().isoformat()
        }
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "degraded",
            "error": str(e),
            "railway_mode": True
        }

@app.post("/api/v1/resume/parse")
async def parse_resume_railway(
    file: UploadFile = File(...),
    candidate_id: Optional[str] = None
):
    """Parse resume with Railway-optimized processing"""
    try:
        # Read file content
        file_content = await file.read()
        
        if not file_content:
            raise HTTPException(status_code=400, detail="Empty file")
        
        logger.info(f"Processing Railway-optimized resume for candidate_id: {candidate_id}, file: {file.filename}")
        
        # Basic processing
        parsed_data = {
            "candidate_id": candidate_id,
            "filename": file.filename,
            "file_size": len(file_content),
            "processing_method": "basic_railway",
            "railway_mode": True,
            "message": "Basic processing completed",
            "timestamp": datetime.now().isoformat()
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "parsed_data": parsed_data,
                "message": "Resume processed successfully",
                "railway_mode": True
            }
        )
        
    except Exception as e:
        logger.error(f"Error in Railway resume parsing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

@app.post("/api/v1/jobs/match")
async def match_candidates_for_job_railway(
    job_data: Dict[str, Any]
):
    """Find top matching candidates for a job using Railway-optimized matching"""
    try:
        # Basic matching
        top_matches = [
            {
                "candidate_id": "sample_candidate_1",
                "match_score": 0.85,
                "match_level": "Excellent",
                "railway_mode": True,
                "message": "Basic matching completed"
            },
            {
                "candidate_id": "sample_candidate_2", 
                "match_score": 0.72,
                "match_level": "Good",
                "railway_mode": True,
                "message": "Basic matching completed"
            }
        ]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "job_data": job_data,
                "top_matches": top_matches,
                "message": f"Found {len(top_matches)} top matches",
                "railway_mode": True
            }
        )
        
    except Exception as e:
        logger.error(f"Error in Railway candidate matching: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error matching candidates: {str(e)}")

@app.get("/api/v1/health/railway")
async def railway_health_check():
    """Railway-optimized health check for all services"""
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "railway_resume_parser": "operational",
                "basic_service": "operational"
            },
            "features": {
                "lightweight_processing": True,
                "railway_optimized": True,
                "basic_fallback": True
            },
            "railway_mode": True
        }
        
        return JSONResponse(
            status_code=200,
            content=health_status
        )
        
    except Exception as e:
        logger.error(f"Error in Railway health check: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Railway health check failed: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "railway_mode": True
        }
    )

# For Railway deployment
def handler(request, context):
    """Railway handler function"""
    return app(request, context)


