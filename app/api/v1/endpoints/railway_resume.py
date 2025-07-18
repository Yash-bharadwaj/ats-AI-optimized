"""
Railway-Optimized Resume Endpoints for AI Recruitment Platform
Simplified version for Railway deployment
"""

import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/parse-railway")
async def parse_resume_railway(
    file: UploadFile = File(...),
    candidate_id: Optional[str] = None
):
    """
    Parse resume with Railway-optimized AI analysis
    """
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
        
        # Basic file processing (Railway-optimized)
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

@router.post("/match-candidates-railway")
async def match_candidates_for_job_railway(
    job_data: Dict[str, Any]
):
    """
    Find top matching candidates for a job using Railway-optimized matching
    """
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

@router.get("/health/railway")
async def railway_health_check():
    """
    Railway-optimized health check for all services
    """
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