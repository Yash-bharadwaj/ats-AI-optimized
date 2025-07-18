from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any, List, Optional
import json
import uuid
import re
from datetime import datetime
import logging

from app.core.config import settings
from app.services.groq_service import GroqService
from app.services.vector_service import VectorService
from app.services.file_processors_vercel import FileProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
groq_service = GroqService()
vector_service = VectorService.create_with_groq(groq_service)
file_processor = FileProcessor()

def extract_and_fix_json(response_text: str) -> Dict[str, Any]:
    """
    Enhanced JSON extraction and fixing for resume parsing responses
    """
    try:
        # Remove markdown code blocks
        response_text = response_text.strip()
        
        # Remove ```json or ``` markers
        if response_text.startswith('```'):
            lines = response_text.split('\n')
            json_lines = []
            in_json_block = False
            
            for line in lines:
                if line.strip().startswith('```'):
                    if not in_json_block:
                        in_json_block = True
                        continue
                    else:
                        break
                
                if in_json_block:
                    json_lines.append(line)
            
            response_text = '\n'.join(json_lines)
        
        # Try to find JSON object boundaries more carefully
        brace_count = 0
        start_index = -1
        end_index = -1
        
        for i, char in enumerate(response_text):
            if char == '{':
                if start_index == -1:
                    start_index = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and start_index != -1:
                    end_index = i + 1
                    break
        
        if start_index != -1 and end_index != -1:
            json_text = response_text[start_index:end_index]
        else:
            json_text = response_text.strip()
        
        # Fix common JSON issues
        json_text = fix_common_json_issues(json_text)
        
        # Try parsing
        try:
            return json.loads(json_text)
        except json.JSONDecodeError as e:
            logger.warning(f"Initial JSON parse failed: {e}")
            # Try more aggressive cleaning
            json_text = aggressive_json_cleanup(json_text)
            return json.loads(json_text)
            
    except Exception as e:
        logger.error(f"JSON extraction failed: {str(e)}")
        raise ValueError(f"Could not extract valid JSON: {str(e)}")

def fix_common_json_issues(json_text: str) -> str:
    """Fix common JSON formatting issues"""
    
    # Remove trailing commas before closing brackets/braces
    json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
    
    # Fix null values
    json_text = re.sub(r':\s*null(?=\s*[,}])', r': null', json_text)
    
    # Fix unquoted field names
    json_text = re.sub(r'(?<!")(\w+)(?=\s*:)', r'"\1"', json_text)
    
    # Fix double quotes that may have been added incorrectly
    json_text = re.sub(r'""(\w+)":', r'"\1":', json_text)
    
    # Fix arrays with trailing commas
    json_text = re.sub(r',(\s*\])', r'\1', json_text)
    
    # CRITICAL FIX: Handle unescaped quotes within string values
    json_text = fix_unescaped_quotes_in_strings(json_text)
    
    return json_text

def fix_unescaped_quotes_in_strings(json_text: str) -> str:
    """Fix unescaped quotes within JSON string values"""
    
    # Split the text into lines to process each field individually
    lines = json_text.split('\n')
    fixed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line or line in ['{', '}', '[', ']']:
            fixed_lines.append(line)
            continue
        
        # Check if this line contains a field with a string value
        if ':' in line and '"' in line:
            # Try to fix quotes in string values
            line = fix_quotes_in_line(line)
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def fix_quotes_in_line(line: str) -> str:
    """Fix quotes in a single JSON line"""
    
    # Pattern to match field: "value" pairs
    field_pattern = r'("[\w_]+"):\s*(".*")'
    match = re.match(r'\s*' + field_pattern + r',?\s*$', line)
    
    if match:
        field_name = match.group(1)
        field_value = match.group(2)
        
        # Remove the outer quotes temporarily
        if field_value.startswith('"') and field_value.endswith('"'):
            inner_value = field_value[1:-1]
            
            # Escape any unescaped quotes in the inner value
            # Replace unescaped quotes with escaped quotes
            inner_value = re.sub(r'(?<!\\)"', r'\\"', inner_value)
            
            # Reconstruct the field value
            field_value = f'"{inner_value}"'
            
            # Check if line ends with comma
            comma = ',' if line.rstrip().endswith(',') else ''
            
            return f'    {field_name}: {field_value}{comma}'
    
    return line

def aggressive_json_cleanup(json_text: str) -> str:
    """More aggressive JSON cleanup for severely malformed JSON"""
    
    # Split into lines and fix line by line
    lines = json_text.split('\n')
    fixed_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Skip incomplete lines
        if line.count('"') % 2 != 0 and not line.endswith(',') and not line.endswith('}') and not line.endswith(']'):
            logger.warning(f"Skipping incomplete line: {line}")
            continue
            
        # Fix common issues in individual lines
        if ':' in line and not line.startswith('{') and not line.startswith('}'):
            # Ensure proper quoting around field names
            parts = line.split(':', 1)
            if len(parts) == 2:
                field_name = parts[0].strip().strip('"')
                value = parts[1].strip()
                
                # Handle string values
                if not value.startswith('[') and not value.startswith('{') and value != 'null':
                    if not value.startswith('"'):
                        value = f'"{value.strip(",")}"'
                
                line = f'"{field_name}": {value}'
        
        fixed_lines.append(line)
    
    # Reconstruct JSON
    reconstructed = '\n'.join(fixed_lines)
    
    # Final cleanup
    reconstructed = re.sub(r',(\s*[}\]])', r'\1', reconstructed)
    reconstructed = re.sub(r',(\s*})', r'\1', reconstructed)
    
    return reconstructed

def create_fallback_response(candidate_id: str, extracted_text: str) -> Dict[str, Any]:
    """Create a fallback response when AI parsing fails"""
    return {
        "candidate_id": candidate_id,
        "name": "Unknown",
        "email": "unknown@example.com",
        "telephone": "",
        "current_employer": "",
        "current_position": "",
        "experience_summary": [],
        "educational_qualifications": [],
        "skills": [],
        "extracted_text": extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text,
        "processing_status": "fallback",
        "error_message": "AI parsing failed, using fallback response"
    }

@router.post("/parse")
async def parse_resume(
    file: UploadFile = File(...),
    candidate_id: str = Form(...)
) -> Dict[str, Any]:
    """
    Parse resume file and extract structured information using AI
    """
    try:
        logger.info(f"Processing resume for candidate_id: {candidate_id}, file: {file.filename}")
        
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Check file size
        file_content = await file.read()
        file_size = len(file_content)
        logger.info(f"File size: {file_size} bytes, file extension: {file.filename.split('.')[-1].lower()}")
        
        if not file_processor.validate_file_size(file_size, settings.MAX_FILE_SIZE):
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE} bytes"
            )
        
        # Validate file type
        file_extension = file.filename.split('.')[-1].lower()
        if not file_processor.validate_file_type(file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Only PDF, DOCX, and TXT files are supported."
            )
        
        # Extract text from file
        logger.info("Starting text extraction...")
        extracted_text = await file_processor.extract_text(file_content, file_extension)
        logger.info(f"Text extraction successful. Extracted text length: {len(extracted_text)} characters")
        
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the file")
        
        # Send to Groq AI for parsing
        logger.info("Sending prompt to Groq AI (attempt 1/2)...")
        try:
            ai_response = await groq_service.parse_resume_with_ai(extracted_text, candidate_id)
            logger.info(f"Groq AI response received. Response length: {len(ai_response)} characters")
            
            # Parse JSON response
            parsed_data = extract_and_fix_json(ai_response)
            logger.info("JSON parsing successful")
            
        except Exception as ai_error:
            logger.error(f"AI parsing failed: {str(ai_error)}")
            logger.info("Attempting fallback response...")
            parsed_data = create_fallback_response(candidate_id, extracted_text)
        
        # Generate vector embedding
        logger.info("Generating vector embedding...")
        try:
            await vector_service.store_resume_embedding(candidate_id, extracted_text)
            logger.info("Successfully stored embedding in Milvus")
        except Exception as embedding_error:
            logger.error(f"Failed to store embedding: {str(embedding_error)}")
            # Continue without embedding - this is not critical
        
        # Add metadata
        parsed_data.update({
            "candidate_id": candidate_id,
            "file_name": file.filename,
            "file_size": file_size,
            "processing_timestamp": datetime.now().isoformat(),
            "processing_status": "success"
        })
        
        logger.info(f"Successfully processed resume for candidate_id: {candidate_id}")
        return parsed_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "resume-parser"} 