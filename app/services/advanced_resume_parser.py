"""
Advanced Resume Parser for AI Recruitment Platform
Includes sophisticated AI analysis and extraction capabilities
"""

import logging
import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import httpx
import os
from app.services.advanced_file_processors import advanced_file_processor

logger = logging.getLogger(__name__)

class AdvancedResumeParser:
    """Advanced resume parser with sophisticated AI analysis"""
    
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
        
        # Advanced extraction patterns
        self.patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            'linkedin': r'linkedin\.com/in/[\w-]+',
            'github': r'github\.com/[\w-]+',
            'website': r'https?://(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:/\S*)?'
        }
    
    async def parse_resume_advanced(
        self, 
        file_content: bytes, 
        filename: str,
        candidate_id: str
    ) -> Dict[str, Any]:
        """Parse resume with advanced AI analysis"""
        try:
            logger.info(f"Starting advanced resume parsing for {filename}")
            
            # Process file with advanced capabilities
            file_result = await advanced_file_processor.process_file(file_content, filename)
            text_content = file_result.get('content', '')
            
            if not text_content:
                raise ValueError("No text content extracted from file")
            
            # Extract basic information using patterns
            basic_info = await self._extract_basic_info(text_content)
            
            # Advanced AI analysis
            ai_analysis = await self._perform_ai_analysis(text_content, basic_info)
            
            # Skills analysis
            skills_analysis = await self._analyze_skills(text_content)
            
            # Experience analysis
            experience_analysis = await self._analyze_experience(text_content)
            
            # Education analysis
            education_analysis = await self._analyze_education(text_content)
            
            # Generate comprehensive profile
            profile = await self._generate_comprehensive_profile(
                basic_info, ai_analysis, skills_analysis, 
                experience_analysis, education_analysis
            )
            
            # Add metadata
            profile.update({
                'candidate_id': candidate_id,
                'filename': filename,
                'file_metadata': file_result.get('metadata', {}),
                'processing_method': file_result.get('processing_method', ''),
                'confidence_score': file_result.get('confidence_score', 0.0),
                'parsed_at': datetime.now().isoformat(),
                'text_length': len(text_content),
                'word_count': len(text_content.split())
            })
            
            logger.info(f"Advanced resume parsing completed for {filename}")
            return profile
            
        except Exception as e:
            logger.error(f"Error in advanced resume parsing: {str(e)}")
            raise
    
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
            
            # Extract website
            website_match = re.search(self.patterns['website'], text_content)
            if website_match:
                basic_info['website'] = website_match.group()
            
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
    
    async def _perform_ai_analysis(self, text_content: str, basic_info: Dict[str, Any]) -> Dict[str, Any]:
        """Perform advanced AI analysis using Groq"""
        try:
            if not self.groq_api_key:
                logger.warning("GROQ_API_KEY not configured")
                return {}
            
            # Create comprehensive prompt for AI analysis
            prompt = f"""
            Analyze this resume and extract detailed information in JSON format:
            
            Resume Text:
            {text_content[:3000]}  # Limit for API
            
            Basic Info Found: {basic_info}
            
            Please extract and return ONLY a valid JSON object with these fields:
            {{
                "name": "Full name",
                "email": "Email address",
                "phone": "Phone number",
                "location": "City, State/Country",
                "summary": "Professional summary (2-3 sentences)",
                "current_role": "Current job title",
                "current_company": "Current employer",
                "experience_years": "Total years of experience (number)",
                "skills": ["skill1", "skill2", "skill3"],
                "technologies": ["tech1", "tech2", "tech3"],
                "languages": ["language1", "language2"],
                "certifications": ["cert1", "cert2"],
                "education": [
                    {{
                        "degree": "Degree name",
                        "institution": "University name",
                        "year": "Graduation year",
                        "gpa": "GPA if mentioned"
                    }}
                ],
                "experience": [
                    {{
                        "title": "Job title",
                        "company": "Company name",
                        "duration": "Duration (e.g., '2 years')",
                        "responsibilities": ["responsibility1", "responsibility2"],
                        "achievements": ["achievement1", "achievement2"]
                    }}
                ],
                "projects": [
                    {{
                        "name": "Project name",
                        "description": "Project description",
                        "technologies": ["tech1", "tech2"],
                        "url": "Project URL if mentioned"
                    }}
                ],
                "interests": ["interest1", "interest2"],
                "availability": "Immediate/2 weeks/1 month",
                "salary_expectation": "Expected salary if mentioned",
                "remote_preference": "Remote/Hybrid/On-site preference",
                "relocation_willingness": "Yes/No/Maybe"
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
                        "max_tokens": 2000,
                        "temperature": 0.1
                    },
                    timeout=30.0
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
            logger.error(f"Error in AI analysis: {str(e)}")
            return {}
    
    async def _analyze_skills(self, text_content: str) -> Dict[str, Any]:
        """Analyze skills with categorization"""
        try:
            # Common skill categories
            skill_categories = {
                'programming_languages': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin'],
                'frameworks': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel', 'asp.net'],
                'databases': ['mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'oracle', 'sqlite'],
                'cloud_platforms': ['aws', 'azure', 'gcp', 'heroku', 'digitalocean', 'vercel'],
                'tools': ['git', 'docker', 'kubernetes', 'jenkins', 'jira', 'confluence', 'figma'],
                'languages': ['english', 'spanish', 'french', 'german', 'chinese', 'japanese', 'hindi']
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
    
    async def _analyze_experience(self, text_content: str) -> Dict[str, Any]:
        """Analyze work experience"""
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
                'seniority_level': self._determine_seniority_level(total_years, job_titles)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing experience: {str(e)}")
            return {}
    
    async def _analyze_education(self, text_content: str) -> Dict[str, Any]:
        """Analyze education background"""
        try:
            # Education patterns
            education_patterns = {
                'bachelor': r'bachelor|b\.s\.|b\.a\.|b\.e\.',
                'master': r'master|m\.s\.|m\.a\.|m\.e\.',
                'phd': r'ph\.d\.|doctorate|doctor',
                'associate': r'associate|a\.a\.',
                'high_school': r'high\s*school|h\.s\.'
            }
            
            education_levels = []
            for level, pattern in education_patterns.items():
                if re.search(pattern, text_content, re.IGNORECASE):
                    education_levels.append(level)
            
            return {
                'education_levels': education_levels,
                'highest_degree': self._get_highest_degree(education_levels),
                'education_count': len(education_levels)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing education: {str(e)}")
            return {}
    
    def _determine_seniority_level(self, years: int, job_titles: List[str]) -> str:
        """Determine seniority level based on experience and titles"""
        if years >= 10 or any('senior' in title.lower() for title in job_titles):
            return 'Senior'
        elif years >= 5 or any('lead' in title.lower() for title in job_titles):
            return 'Mid-Level'
        elif years >= 2:
            return 'Junior'
        else:
            return 'Entry-Level'
    
    def _get_highest_degree(self, education_levels: List[str]) -> str:
        """Get highest education degree"""
        degree_hierarchy = ['phd', 'master', 'bachelor', 'associate', 'high_school']
        
        for degree in degree_hierarchy:
            if degree in education_levels:
                return degree
        
        return 'unknown'
    
    async def _generate_comprehensive_profile(
        self,
        basic_info: Dict[str, Any],
        ai_analysis: Dict[str, Any],
        skills_analysis: Dict[str, Any],
        experience_analysis: Dict[str, Any],
        education_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate comprehensive candidate profile"""
        try:
            # Merge all analyses
            profile = {
                'basic_info': basic_info,
                'ai_analysis': ai_analysis,
                'skills_analysis': skills_analysis,
                'experience_analysis': experience_analysis,
                'education_analysis': education_analysis,
                
                # Summary metrics
                'summary': {
                    'total_skills': skills_analysis.get('total_skills', 0),
                    'years_experience': experience_analysis.get('total_years_experience', 0),
                    'seniority_level': experience_analysis.get('seniority_level', 'Unknown'),
                    'highest_education': education_analysis.get('highest_degree', 'Unknown'),
                    'skill_categories': skills_analysis.get('skill_categories', 0)
                },
                
                # Confidence scores
                'confidence_scores': {
                    'basic_info': len(basic_info) / 5,  # 5 basic fields
                    'ai_analysis': len(ai_analysis) / 15,  # 15 AI fields
                    'skills': skills_analysis.get('total_skills', 0) / 20,  # Normalized
                    'experience': min(experience_analysis.get('total_years_experience', 0) / 10, 1.0),
                    'education': education_analysis.get('education_count', 0) / 3
                }
            }
            
            # Calculate overall confidence
            confidence_scores = profile['confidence_scores'].values()
            profile['overall_confidence'] = sum(confidence_scores) / len(confidence_scores)
            
            return profile
            
        except Exception as e:
            logger.error(f"Error generating comprehensive profile: {str(e)}")
            return {}

# Global instance
advanced_resume_parser = AdvancedResumeParser() 