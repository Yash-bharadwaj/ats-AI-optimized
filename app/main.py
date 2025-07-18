from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from dotenv import load_dotenv
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.api.v1.api import api_router
from app.core.config import settings
from app.services.vector_service import vector_service

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
    ]
)

# Set specific loggers to different levels if needed
logging.getLogger("app.api.v1.endpoints.resume").setLevel(logging.DEBUG)
logging.getLogger("app.services.file_processors").setLevel(logging.DEBUG)
logging.getLogger("app.services.groq_service").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",  # Updated version for advanced features
    description="AI Recruitment Platform with Advanced OCR, AI Analysis, and Smart Matching",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set up CORS middleware
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
        # Initialize vector service
        await vector_service.initialize_collections()
        logger.info("✅ Vector service connected successfully on startup")
    except Exception as e:
        logger.error(f"❌ Failed to connect vector service on startup: {e}")

@app.get("/")
async def root():
    """Root endpoint with platform information"""
    return {
        "message": "AI Recruitment Platform - Advanced Edition",
        "version": "2.0.0",
        "features": [
            "Advanced OCR and Image Processing",
            "Sophisticated AI Analysis", 
            "Advanced Matching Algorithms",
            "Multi-format File Support",
            "Comprehensive Analytics"
        ],
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check vector service connection
        await vector_service.initialize_collections()
        logger.info("✅ Vector service connected successfully on startup")
        
        return {
            "status": "healthy",
            "message": "API is running",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "features": "Advanced OCR, AI Analysis, Smart Matching"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "unhealthy",
                "message": f"Health check failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# For Vercel deployment
def handler(request, context):
    return app(request, context)


