"""
Railway-Optimized Resume Parser for AI Recruitment Platform
Simplified version for Railway deployment
"""

import logging
import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
import os

logger = logging.getLogger(__name__)

class RailwayResumeParser:
    """Railway-optimized resume parser with basic capabilities"""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        
        # Basic extraction patterns
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'linkedin': r'linkedin\.com/in/[\w-]+',
            'github': r'github\.com/[\w-]+',
            'website': r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/\S*)?'
        }
    
    async def parse_resume_railway(
        self, 
        file_content: bytes, 
        filename: str,
        candidate_id: str
    ) -> Dict[str, Any]:
        """Parse resume with Railway-optimized analysis"""
        try:
            logger.info(f"Starting Railway-optimized resume parsing for {filename}")
            
            # Basic file processing
            text_content = await self._extract_text_basic(file_content, filename)
            
            if not text_content:
                raise ValueError("No text content extracted from file")
            
            # Extract basic information using patterns
            basic_info = await self._extract_basic_info(text_content)
            
            # Lightweight AI analysis
            ai_analysis = await self._perform_ai_analysis_basic(text_content, basic_info)
            
            # Skills analysis
            skills_analysis = await self._analyze_skills_basic(text_content)
            
            # Experience analysis
            experience_analysis = await self._analyze_experience_basic(text_content)
            
            # Generate basic profile
            profile = await self._generate_basic_profile(
                basic_info, ai_analysis, skills_analysis, experience_analysis
            )
            
            # Add metadata
            profile.update({
                'candidate_id': candidate_id,
                'filename': filename,
                'parsed_at': datetime.now().isoformat(),
                'text_length': len(text_content),
                'word_count': len(text_content.split()),
                'railway_mode': True
            })
            
            logger.info(f"Railway-optimized resume parsing completed for {filename}")
            return profile
            
        except Exception as e:
            logger.error(f"Error in Railway resume parsing: {str(e)}")
            raise
    
    async def _extract_text_basic(self, file_content: bytes, filename: str) -> str:
        """Extract text from file with basic processing"""
        try:
            # Try to process with Railway file processor
            try:
                from app.services.railway_file_processors import railway_file_processor
                file_result = await railway_file_processor.process_file(file_content, filename)
                return file_result.get('content', '')
            except Exception as e:
                logger.warning(f"Railway file processor not available: {str(e)}")
                
                # Fallback to basic text extraction
                try:
                    return file_content.decode('utf-8')
                except:
                    return file_content.decode('latin-1')
                    
        except Exception as e:
            logger.error(f"Error extracting text: {str(e)}")
            return ""
    
    async def _extract_basic_info(self, text_content: str) -> Dict[str, Any]:
        """Extract basic information using regex patterns"""
        try:
            basic_info = {}
            
            # Extract email
            email_match = re.search(self.patterns['email'], text_content)
            if email_match:
                basic_info['email'] = email_match.group()
            
            # Extract phone
            phone_match = re.search(self.patterns['phone'], text_content)
            if phone_match:
                basic_info['phone'] = phone_match.group()
            
            # Extract LinkedIn
            linkedin_match = re.search(self.patterns['linkedin'], text_content)
            if linkedin_match:
                basic_info['linkedin'] = linkedin_match.group()
            
            # Extract GitHub
            github_match = re.search(self.patterns['github'], text_content)
            if github_match:
                basic_info['github'] = github_match.group()
            
            # Extract name (first few lines)
            lines = text_content.split('\n')[:10]
            for line in lines:
                line = line.strip()
                if line and not any(keyword in line.lower() for keyword in ['email', 'phone', 'linkedin', 'github', 'experience', 'education']):
                    if len(line.split()) <= 4:  # Likely a name
                        basic_info['name'] = line
                        break
            
            return basic_info
            
        except Exception as e:
            logger.error(f"Error extracting basic info: {str(e)}")
            return {}
    
    async def _perform_ai_analysis_basic(self, text_content: str, basic_info: Dict[str, Any]) -> Dict[str, Any]:
        """Perform basic AI analysis using Groq"""
        try:
            if not self.groq_api_key:
                logger.warning("GROQ_API_KEY not configured")
                return {}
            
            # Create basic prompt for AI analysis
            prompt = f"""
            Analyze this resume and extract key information in JSON format:
            
            Resume Text:
            {text_content[:1500]}  # Shorter limit for Railway
            
            Basic Info Found: {basic_info}
            
            Please extract and return ONLY a valid JSON object with these fields:
            {{
                "name": "Full name",
                "email": "Email address",
                "phone": "Phone number",
                "location": "City, State/Country",
                "summary": "Professional summary (1-2 sentences)",
                "current_role": "Current job title",
                "current_company": "Current employer",
                "experience_years": "Total years of experience (number)",
                "skills": ["skill1", "skill2", "skill3"],
                "technologies": ["tech1", "tech2", "tech3"]
            }}
            
            Return ONLY the JSON object, no additional text.
            """
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.groq_api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [{"role": "user", "content": prompt}],
                        "max_tokens": 1000,
                        "temperature": 0.1
                    },
                    timeout=15.0
                )
                
                if response.status_code != 200:
                    logger.error(f"Groq API error: {response.status_code}")
                    return {}
                
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Extract JSON from response
                try:
                    start = content.find('{')
                    end = content.rfind('}') + 1
                    if start != -1 and end != 0:
                        json_str = content[start:end]
                        return json.loads(json_str)
                    else:
                        logger.error("Could not parse JSON from AI response")
                        return {}
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decode error: {str(e)}")
                    return {}
                    
        except Exception as e:
            logger.error(f"Error in basic AI analysis: {str(e)}")
            return {}
    
    async def _analyze_skills_basic(self, text_content: str) -> Dict[str, Any]:
        """Analyze skills with basic categorization"""
        try:
            # Common skill categories
            skill_categories = {
                'programming_languages': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin'],
                'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel', 'asp.net'],
                'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite'],
                'cloud_platforms': ['aws', 'azure', 'gcp', 'heroku', 'digitalocean', 'vercel'],
                'tools': ['git', 'docker', 'kubernetes', 'jenkins', 'jira', 'confluence', 'figma']
            }
            
            text_lower = text_content.lower()
            found_skills = {}
            
            for category, skills in skill_categories.items():
                category_skills = []
                for skill in skills:
                    if skill in text_lower:
                        category_skills.append(skill)
                if category_skills:
                    found_skills[category] = category_skills
            
            return {
                'categorized_skills': found_skills,
                'total_skills': sum(len(skills) for skills in found_skills.values()),
                'skill_categories': len(found_skills)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing skills: {str(e)}")
            return {}
    
    async def _analyze_experience_basic(self, text_content: str) -> Dict[str, Any]:
        """Analyze work experience with basic approach"""
        try:
            # Extract experience patterns
            experience_patterns = [
                r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?experience',
                r'experience:\s*(\d+)',
                r'(\d+)\s*years?\s*in\s*the\s*field'
            ]
            
            total_years = 0
            for pattern in experience_patterns:
                match = re.search(pattern, text_content, re.IGNORECASE)
                if match:
                    total_years = int(match.group(1))
                    break
            
            # Count job titles
            job_titles = re.findall(r'(?:senior|junior|lead|principal|staff)\s+\w+', text_content, re.IGNORECASE)
            
            return {
                'total_years_experience': total_years,
                'job_titles_found': len(job_titles),
                'seniority_level': self._determine_seniority_level_basic(total_years, job_titles)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing experience: {str(e)}")
            return {}
    
    def _determine_seniority_level_basic(self, years: int, job_titles: List[str]) -> str:
        """Determine seniority level based on experience and titles"""
        if years >= 10 or any('senior' in title.lower() for title in job_titles):
            return 'Senior'
        elif years >= 5 or any('lead' in title.lower() for title in job_titles):
            return 'Mid-Level'
        elif years >= 2:
            return 'Junior'
        else:
            return 'Entry-Level'
    
    async def _generate_basic_profile(
        self,
        basic_info: Dict[str, Any],
        ai_analysis: Dict[str, Any],
        skills_analysis: Dict[str, Any],
        experience_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate basic candidate profile for Railway"""
        try:
            # Merge all analyses
            profile = {
                'basic_info': basic_info,
                'ai_analysis': ai_analysis,
                'skills_analysis': skills_analysis,
                'experience_analysis': experience_analysis,
                
                # Summary metrics
                'summary': {
                    'total_skills': skills_analysis.get('total_skills', 0),
                    'years_experience': experience_analysis.get('total_years_experience', 0),
                    'seniority_level': experience_analysis.get('seniority_level', 'Unknown'),
                    'skill_categories': skills_analysis.get('skill_categories', 0)
                },
                
                # Confidence scores
                'confidence_scores': {
                    'basic_info': len(basic_info) / 5,  # 5 basic fields
                    'ai_analysis': len(ai_analysis) / 8,  # 8 AI fields for Railway
                    'skills': skills_analysis.get('total_skills', 0) / 20,  # Normalized
                    'experience': min(experience_analysis.get('total_years_experience', 0) / 10, 1.0)
                }
            }
            
            # Calculate overall confidence
            confidence_scores = profile['confidence_scores'].values()
            profile['overall_confidence'] = sum(confidence_scores) / len(confidence_scores)
            
            return profile
            
        except Exception as e:
            logger.error(f"Error generating basic profile: {str(e)}")
            return {}

# Global instance
railway_resume_parser = RailwayResumeParser() 