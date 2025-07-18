"""
Main FastAPI application for AI Recruitment Platform
Railway-optimized version with minimal dependencies
"""

import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Recruitment Platform",
    version="2.0.0",
    description="AI Recruitment Platform with Railway Optimization",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
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
        
        # Try to import and initialize services
        try:
            from app.services.vector_service import vector_service
            await vector_service.initialize()
            logger.info("✅ Vector service connected successfully")
        except Exception as e:
            logger.warning(f"⚠️ Vector service not available: {str(e)}")
        
        try:
            from app.services.groq_service import groq_service
            logger.info("✅ Groq service initialized")
        except Exception as e:
            logger.warning(f"⚠️ Groq service not available: {str(e)}")
        
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
        # Basic health check
        health_status = {
            "status": "healthy",
            "services": {
                "api": "operational",
                "railway_mode": True
            },
            "version": "2.0.0",
            "railway_optimized": True
        }
        
        # Try to check vector service if available
        try:
            from app.services.vector_service import vector_service
            if vector_service.is_connected():
                health_status["services"]["vector_service"] = "healthy"
            else:
                health_status["services"]["vector_service"] = "unhealthy"
        except:
            health_status["services"]["vector_service"] = "unavailable"
        
        return health_status
        
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

# Include API routes if available
try:
    from app.api.v1.api import api_router
    app.include_router(api_router, prefix="/api/v1")
    logger.info("✅ API routes loaded successfully")
except Exception as e:
    logger.warning(f"⚠️ API routes not available: {str(e)}")
    
    # Create basic endpoints if API routes fail
    @app.post("/api/v1/railway/parse-railway")
    async def parse_resume_railway_fallback():
        return {
            "success": False,
            "message": "Railway-optimized parsing not available",
            "railway_mode": True
        }
    
    @app.get("/api/v1/railway/health/railway")
    async def railway_health_check_fallback():
        return {
            "status": "degraded",
            "message": "Railway services not fully available",
            "railway_mode": True
        }


