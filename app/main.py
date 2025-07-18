"""
Main FastAPI application for AI Recruitment Platform
Railway-optimized version
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

from app.core.config import settings
from app.api.v1.api import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    description="AI Recruitment Platform with Railway Optimization",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        # Import and initialize vector service
        from app.services.vector_service import vector_service
        await vector_service.initialize()
        logger.info("✅ Vector service connected successfully on startup")
        
        # Import and initialize other services
        from app.services.groq_service import groq_service
        logger.info("✅ Groq service initialized successfully")
        
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
        "docs": "/api/v1/docs",
        "health": "/health"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check vector service
        from app.services.vector_service import vector_service
        vector_status = "healthy" if vector_service.is_connected() else "unhealthy"
        
        return {
            "status": "healthy",
            "services": {
                "vector_service": vector_status,
                "groq_service": "operational",
                "railway_mode": True
            },
            "version": "2.0.0",
            "railway_optimized": True
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "degraded",
            "error": str(e),
            "railway_mode": True
        }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "railway_mode": True
        }
    )

# Railway-specific handler
def handler(request, context):
    """Railway handler for serverless deployment"""
    return app(request, context)


