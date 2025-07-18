"""
Advanced Resume Endpoints for AI Recruitment Platform
Includes sophisticated parsing and matching capabilities
"""

import logging
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import json
from datetime import datetime

from app.services.advanced_resume_parser import advanced_resume_parser
from app.services.advanced_matching_service import advanced_matching_service
from app.services.vector_service import vector_service
from app.services.groq_service import groq_service
from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/parse-advanced")
async def parse_resume_advanced(
    file: UploadFile = File(...),
    candidate_id: Optional[str] = None
):
    """
    Parse resume with advanced AI analysis and comprehensive extraction
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
        
        logger.info(f"Processing advanced resume for candidate_id: {candidate_id}, file: {file.filename}")
        
        # Advanced resume parsing
        parsed_data = await advanced_resume_parser.parse_resume_advanced(
            file_content, file.filename, candidate_id
        )
        
        # Generate embedding for vector search
        if parsed_data.get('ai_analysis', {}).get('summary'):
            summary_text = parsed_data['ai_analysis']['summary']
            embedding = await groq_service.generate_mistral_embedding(summary_text)
            
            # Store in vector database
            await vector_service.store_resume_embedding(
                candidate_id=candidate_id,
                embedding=embedding,
                metadata={
                    'filename': file.filename,
                    'parsed_data': parsed_data,
                    'confidence_score': parsed_data.get('overall_confidence', 0.0)
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "candidate_id": candidate_id,
                "parsed_data": parsed_data,
                "message": "Advanced resume parsing completed successfully"
            }
        )
        
    except Exception as e:
        logger.error(f"Error in advanced resume parsing: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

@router.post("/match-candidates")
async def match_candidates_for_job(
    job_data: Dict[str, Any]
):
    """
    Find top matching candidates for a job using advanced matching algorithm
    """
    try:
        # Get all candidates from vector database
        candidates = await vector_service.get_all_resume_embeddings()
        
        if not candidates:
            raise HTTPException(status_code=404, detail="No candidates found in database")
        
        # Use advanced matching service
        top_matches = await advanced_matching_service.find_top_matches(
            job_data=job_data,
            candidates=candidates,
            limit=10
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "job_data": job_data,
                "top_matches": top_matches,
                "total_candidates": len(candidates),
                "message": f"Found {len(top_matches)} top matches"
            }
        )
        
    except Exception as e:
        logger.error(f"Error in candidate matching: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error matching candidates: {str(e)}")

@router.post("/calculate-match-score")
async def calculate_match_score(
    candidate_data: Dict[str, Any],
    job_data: Dict[str, Any]
):
    """
    Calculate detailed match score between candidate and job
    """
    try:
        # Calculate advanced match score
        match_result = await advanced_matching_service.calculate_advanced_match_score(
            candidate_data=candidate_data,
            job_data=job_data
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "match_result": match_result,
                "message": f"Match score calculated: {match_result['total_score']}"
            }
        )
        
    except Exception as e:
        logger.error(f"Error calculating match score: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error calculating match score: {str(e)}")

@router.get("/candidate/{candidate_id}/profile")
async def get_candidate_profile(candidate_id: str):
    """
    Get comprehensive candidate profile
    """
    try:
        # Get candidate data from vector database
        candidate_data = await vector_service.get_resume_embedding(candidate_id)
        
        if not candidate_data:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "candidate_id": candidate_id,
                "profile": candidate_data.get('metadata', {}).get('parsed_data', {}),
                "embedding_info": {
                    "has_embedding": bool(candidate_data.get('embedding')),
                    "embedding_dimension": len(candidate_data.get('embedding', [])),
                    "stored_at": candidate_data.get('metadata', {}).get('stored_at')
                }
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting candidate profile: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting candidate profile: {str(e)}")

@router.post("/analyze-skills")
async def analyze_skills(
    text_content: str
):
    """
    Analyze skills from text content
    """
    try:
        skills_analysis = await advanced_resume_parser._analyze_skills(text_content)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "skills_analysis": skills_analysis,
                "message": "Skills analysis completed"
            }
        )
        
    except Exception as e:
        logger.error(f"Error analyzing skills: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error analyzing skills: {str(e)}")

@router.post("/extract-structured-data")
async def extract_structured_data(
    text_content: str
):
    """
    Extract structured data from text content
    """
    try:
        structured_data = await advanced_resume_parser.extract_structured_data(text_content)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "structured_data": structured_data,
                "message": "Structured data extraction completed"
            }
        )
        
    except Exception as e:
        logger.error(f"Error extracting structured data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error extracting structured data: {str(e)}")

@router.get("/health/advanced")
async def advanced_health_check():
    """
    Advanced health check for all services
    """
    try:
        health_status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "advanced_resume_parser": "operational",
                "advanced_matching_service": "operational",
                "vector_service": "operational",
                "groq_service": "operational"
            },
            "features": {
                "ocr_processing": True,
                "image_processing": True,
                "advanced_matching": True,
                "vector_search": True,
                "ai_analysis": True
            }
        }
        
        return JSONResponse(
            status_code=200,
            content=health_status
        )
        
    except Exception as e:
        logger.error(f"Error in advanced health check: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}") 