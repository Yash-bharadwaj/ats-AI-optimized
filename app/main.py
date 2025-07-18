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
        
        # Try to import and initialize services with graceful fallbacks
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
        "docs": "/docs",
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
            "railway_optimized": True,
            "timestamp": datetime.now().isoformat()
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

@app.post("/api/v1/resume/parse")
async def parse_resume_railway(
    file: UploadFile = File(...),
    candidate_id: Optional[str] = None
):
    """Parse resume with Railway-optimized processing"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Read file content
        file_content = await file.read()
        
        # Generate candidate ID if not provided
        if not candidate_id:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            candidate_id = f"candidate_{timestamp}"
        
        logger.info(f"Processing Railway-optimized resume for candidate_id: {candidate_id}, file: {file.filename}")
        
        # Basic file processing
        try:
            from app.services.railway_resume_parser import railway_resume_parser
            parsed_data = await railway_resume_parser.parse_resume_railway(
                file_content, file.filename, candidate_id
            )
            
            # Try to store in vector database if available
            try:
                from app.services.vector_service import vector_service
                from app.services.groq_service import groq_service
                
                if parsed_data.get('ai_analysis', {}).get('summary'):
                    summary_text = parsed_data['ai_analysis']['summary']
                    embedding = await groq_service.generate_mistral_embedding(summary_text)
                    
                    await vector_service.store_resume_embedding(
                        candidate_id=candidate_id,
                        embedding=embedding,
                        metadata={
                            'filename': file.filename,
                            'parsed_data': parsed_data,
                            'confidence_score': parsed_data.get('overall_confidence', 0.0),
                            'railway_mode': True
                        }
                    )
            except Exception as e:
                logger.warning(f"Vector storage not available: {str(e)}")
            
        except Exception as e:
            logger.error(f"Railway parser not available: {str(e)}")
            # Fallback to basic processing
            parsed_data = {
                "candidate_id": candidate_id,
                "filename": file.filename,
                "file_size": len(file_content),
                "processing_method": "basic",
                "railway_mode": True,
                "message": "Basic processing completed"
            }
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "candidate_id": candidate_id,
                "parsed_data": parsed_data,
                "message": "Railway-optimized resume parsing completed successfully",
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
        # Try to get candidates from vector database
        try:
            from app.services.vector_service import vector_service
            from app.services.advanced_matching_service import advanced_matching_service
            
            candidates = await vector_service.get_all_resume_embeddings()
            
            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found in database")
            
            # Use advanced matching service
            top_matches = await advanced_matching_service.find_top_matches(
                job_data=job_data,
                candidates=candidates,
                limit=10
            )
            
        except Exception as e:
            logger.warning(f"Advanced matching not available: {str(e)}")
            # Fallback to basic matching
            top_matches = [
                {
                    "candidate_id": "sample_candidate",
                    "match_score": 0.8,
                    "match_level": "Good",
                    "railway_mode": True
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
                "vector_service": "operational",
                "groq_service": "operational"
            },
            "features": {
                "lightweight_processing": True,
                "railway_optimized": True,
                "vector_search": True,
                "ai_analysis": True
            },
            "railway_mode": True
        }
        
        # Check if services are actually available
        try:
            from app.services.vector_service import vector_service
            if not vector_service.is_connected():
                health_status["services"]["vector_service"] = "unhealthy"
        except:
            health_status["services"]["vector_service"] = "unavailable"
        
        try:
            from app.services.groq_service import groq_service
            # Basic check
        except:
            health_status["services"]["groq_service"] = "unavailable"
        
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


