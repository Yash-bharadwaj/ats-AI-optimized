from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging
from dotenv import load_dotenv
import sys
import json
import httpx
from typing import Dict, Any

# Add the parent directory to the path so we can import from app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Recruitment Platform",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Recruitment Platform API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/v1/docs")
async def api_docs():
    return {"message": "API documentation available at /docs"}

@app.post("/api/v1/resume/parse")
async def parse_resume(file: UploadFile = File(...)):
    """Parse resume using AI - Ultra minimal version for Vercel"""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Check file size (4MB limit)
        file_size = 0
        content = await file.read()
        file_size = len(content)
        
        if file_size > 4 * 1024 * 1024:  # 4MB
            raise HTTPException(status_code=400, detail="File too large. Max 4MB")
        
        # Extract text based on file type
        text_content = await extract_text_from_file(content, file.filename)
        
        # Parse with Groq AI
        parsed_data = await parse_with_groq(text_content)
        
        # Generate embedding with Mistral (simplified)
        embedding = await generate_embedding(text_content)
        
        return {
            "success": True,
            "candidate_id": f"candidate_{os.getenv('PROJECT_NAME', 'ai_recruitment')}",
            "parsed_data": parsed_data,
            "embedding_generated": bool(embedding),
            "file_size": file_size,
            "text_length": len(text_content)
        }
        
    except Exception as e:
        logger.error(f"Error parsing resume: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

async def extract_text_from_file(content: bytes, filename: str) -> str:
    """Extract text from file - Ultra minimal version"""
    try:
        if filename.lower().endswith('.pdf'):
            import PyPDF2
            import io
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        elif filename.lower().endswith('.docx'):
            import docx
            import io
            doc = docx.Document(io.BytesIO(content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        elif filename.lower().endswith('.txt'):
            return content.decode('utf-8')
        else:
            raise ValueError(f"Unsupported file type: {filename}")
    except Exception as e:
        logger.error(f"Error extracting text: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error extracting text: {str(e)}")

async def parse_with_groq(text_content: str) -> Dict[str, Any]:
    """Parse resume with Groq AI - Ultra minimal version"""
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise HTTPException(status_code=500, detail="GROQ_API_KEY not configured")
        
        prompt = f"""
        Extract the following information from this resume in JSON format:
        - name
        - email
        - telephone
        - current_employer
        - experience_years
        - skills (list)
        - education
        - location
        
        Resume text:
        {text_content[:3000]}  # Limit to first 3000 chars for Vercel
        
        Return only valid JSON.
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-8b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000,
                    "temperature": 0.1
                },
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Groq API error")
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Try to extract JSON from response
            try:
                # Find JSON in the response
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    return json.loads(json_str)
                else:
                    return {"error": "Could not parse JSON from response", "raw_response": content}
            except json.JSONDecodeError:
                return {"error": "Invalid JSON response", "raw_response": content}
                
    except Exception as e:
        logger.error(f"Error with Groq API: {str(e)}")
        return {"error": f"Groq API error: {str(e)}"}

async def generate_embedding(text_content: str) -> list:
    """Generate embedding with Mistral AI - Ultra minimal version"""
    try:
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        if not mistral_api_key:
            logger.warning("MISTRAL_API_KEY not configured, skipping embedding")
            return []
        
        # Limit text for Vercel
        limited_text = text_content[:1000]
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.mistral.ai/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {mistral_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistral-embed",
                    "input": limited_text
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["data"][0]["embedding"]
            else:
                logger.warning(f"Mistral API error: {response.status_code}")
                return []
                
    except Exception as e:
        logger.error(f"Error with Mistral API: {str(e)}")
        return []

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    logger.error(f"Request URL: {request.url}")
    logger.error(f"Request method: {request.method}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# For Vercel deployment - this is the main handler
from mangum import Mangum

# Create the ASGI adapter for AWS Lambda/Vercel
handler = Mangum(app) 