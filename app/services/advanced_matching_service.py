"""
Advanced Matching Service for AI Recruitment Platform
Includes sophisticated matching algorithms and scoring systems
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import re
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class AdvancedMatchingService:
    """Advanced matching service with sophisticated algorithms"""
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.scaler = StandardScaler()
        
        # Advanced scoring weights
        self.weights = {
            'skills_match': 0.35,
            'experience_match': 0.25,
            'location_match': 0.15,
            'education_match': 0.10,
            'salary_match': 0.05,
            'culture_match': 0.05,
            'availability_match': 0.05
        }
    
    async def calculate_advanced_match_score(
        self, 
        candidate_data: Dict[str, Any], 
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calculate advanced match score with multiple factors"""
        try:
            scores = {}
            
            # Skills matching with semantic analysis
            scores['skills_match'] = await self._calculate_skills_match(
                candidate_data.get('skills', []),
                job_data.get('required_skills', [])
            )
            
            # Experience matching
            scores['experience_match'] = await self._calculate_experience_match(
                candidate_data.get('experience_years', 0),
                job_data.get('min_experience', 0),
                job_data.get('max_experience', 10)
            )
            
            # Location matching
            scores['location_match'] = await self._calculate_location_match(
                candidate_data.get('location', ''),
                job_data.get('location', ''),
                job_data.get('remote_work', False)
            )
            
            # Education matching
            scores['education_match'] = await self._calculate_education_match(
                candidate_data.get('education', []),
                job_data.get('education_requirements', [])
            )
            
            # Salary matching
            scores['salary_match'] = await self._calculate_salary_match(
                candidate_data.get('expected_salary', 0),
                job_data.get('salary_range', {})
            )
            
            # Culture matching
            scores['culture_match'] = await self._calculate_culture_match(
                candidate_data.get('preferences', {}),
                job_data.get('company_culture', {})
            )
            
            # Availability matching
            scores['availability_match'] = await self._calculate_availability_match(
                candidate_data.get('availability', ''),
                job_data.get('job_type', 'full_time')
            )
            
            # Calculate weighted total score
            total_score = sum(
                scores[factor] * self.weights[factor] 
                for factor in self.weights.keys()
            )
            
            return {
                'total_score': round(total_score, 3),
                'detailed_scores': scores,
                'weights': self.weights,
                'match_level': self._get_match_level(total_score),
                'recommendations': await self._generate_recommendations(scores),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating advanced match score: {str(e)}")
            raise
    
    async def _calculate_skills_match(
        self, 
        candidate_skills: List[str], 
        required_skills: List[str]
    ) -> float:
        """Calculate skills match with semantic analysis"""
        try:
            if not candidate_skills or not required_skills:
                return 0.0
            
            # Normalize skills
            candidate_skills = [skill.lower().strip() for skill in candidate_skills]
            required_skills = [skill.lower().strip() for skill in required_skills]
            
            # Exact matches
            exact_matches = set(candidate_skills) & set(required_skills)
            exact_score = len(exact_matches) / len(required_skills)
            
            # Semantic similarity using TF-IDF
            all_skills = candidate_skills + required_skills
            if len(all_skills) > 1:
                try:
                    tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_skills)
                    similarity_matrix = cosine_similarity(tfidf_matrix)
                    
                    # Calculate semantic similarity
                    semantic_score = np.mean(similarity_matrix[:len(candidate_skills), len(candidate_skills):])
                except:
                    semantic_score = 0.0
            else:
                semantic_score = 0.0
            
            # Combined score (70% exact, 30% semantic)
            final_score = 0.7 * exact_score + 0.3 * semantic_score
            
            return min(final_score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating skills match: {str(e)}")
            return 0.0
    
    async def _calculate_experience_match(
        self, 
        candidate_years: int, 
        min_required: int, 
        max_required: int
    ) -> float:
        """Calculate experience match with sophisticated logic"""
        try:
            if candidate_years < min_required:
                # Underqualified
                return max(0.0, 1.0 - (min_required - candidate_years) * 0.2)
            elif candidate_years <= max_required:
                # Perfect range
                return 1.0
            else:
                # Overqualified - still good but not perfect
                overqualification = candidate_years - max_required
                return max(0.7, 1.0 - overqualification * 0.1)
                
        except Exception as e:
            logger.error(f"Error calculating experience match: {str(e)}")
            return 0.0
    
    async def _calculate_location_match(
        self, 
        candidate_location: str, 
        job_location: str, 
        remote_work: bool
    ) -> float:
        """Calculate location match with remote work consideration"""
        try:
            if remote_work:
                # Remote work is more flexible
                return 0.8  # Good score for remote positions
            
            # Simple location matching (can be enhanced with geocoding)
            candidate_location = candidate_location.lower().strip()
            job_location = job_location.lower().strip()
            
            if candidate_location == job_location:
                return 1.0
            elif candidate_location in job_location or job_location in candidate_location:
                return 0.8
            else:
                # Check for same city/state
                candidate_parts = candidate_location.split(',')
                job_parts = job_location.split(',')
                
                if len(candidate_parts) > 1 and len(job_parts) > 1:
                    if candidate_parts[1].strip() == job_parts[1].strip():
                        return 0.6  # Same state/region
                
                return 0.3  # Different locations
                
        except Exception as e:
            logger.error(f"Error calculating location match: {str(e)}")
            return 0.0
    
    async def _calculate_education_match(
        self, 
        candidate_education: List[str], 
        required_education: List[str]
    ) -> float:
        """Calculate education match"""
        try:
            if not required_education:
                return 1.0  # No education requirements
            
            if not candidate_education:
                return 0.0  # No education provided
            
            # Normalize education levels
            education_levels = {
                'high school': 1,
                'associate': 2,
                'bachelor': 3,
                'master': 4,
                'phd': 5,
                'doctorate': 5
            }
            
            candidate_levels = []
            for edu in candidate_education:
                for level, score in education_levels.items():
                    if level in edu.lower():
                        candidate_levels.append(score)
                        break
            
            required_levels = []
            for edu in required_education:
                for level, score in education_levels.items():
                    if level in edu.lower():
                        required_levels.append(score)
                        break
            
            if not candidate_levels:
                return 0.0
            
            if not required_levels:
                return 1.0
            
            max_candidate = max(candidate_levels)
            min_required = min(required_levels)
            
            if max_candidate >= min_required:
                return 1.0
            else:
                return max(0.0, 1.0 - (min_required - max_candidate) * 0.3)
                
        except Exception as e:
            logger.error(f"Error calculating education match: {str(e)}")
            return 0.0
    
    async def _calculate_salary_match(
        self, 
        expected_salary: float, 
        salary_range: Dict[str, float]
    ) -> float:
        """Calculate salary match"""
        try:
            if not salary_range or not expected_salary:
                return 0.5  # Neutral score
            
            min_salary = salary_range.get('min', 0)
            max_salary = salary_range.get('max', float('inf'))
            
            if min_salary <= expected_salary <= max_salary:
                return 1.0
            elif expected_salary < min_salary:
                # Candidate expects less - might be good for company
                return 0.8
            else:
                # Candidate expects more - might be negotiable
                return max(0.3, 1.0 - (expected_salary - max_salary) / max_salary * 0.5)
                
        except Exception as e:
            logger.error(f"Error calculating salary match: {str(e)}")
            return 0.5
    
    async def _calculate_culture_match(
        self, 
        candidate_preferences: Dict[str, Any], 
        company_culture: Dict[str, Any]
    ) -> float:
        """Calculate culture match"""
        try:
            if not candidate_preferences or not company_culture:
                return 0.5  # Neutral score
            
            # Simple culture matching (can be enhanced)
            matching_factors = 0
            total_factors = 0
            
            for factor in ['work_style', 'values', 'environment']:
                if factor in candidate_preferences and factor in company_culture:
                    total_factors += 1
                    if candidate_preferences[factor] == company_culture[factor]:
                        matching_factors += 1
            
            if total_factors == 0:
                return 0.5
            
            return matching_factors / total_factors
            
        except Exception as e:
            logger.error(f"Error calculating culture match: {str(e)}")
            return 0.5
    
    async def _calculate_availability_match(
        self, 
        candidate_availability: str, 
        job_type: str
    ) -> float:
        """Calculate availability match"""
        try:
            if not candidate_availability:
                return 0.5
            
            availability_lower = candidate_availability.lower()
            
            if job_type == 'full_time':
                if 'full' in availability_lower or 'immediate' in availability_lower:
                    return 1.0
                elif 'part' in availability_lower:
                    return 0.3
                else:
                    return 0.7
            elif job_type == 'part_time':
                if 'part' in availability_lower:
                    return 1.0
                elif 'full' in availability_lower:
                    return 0.8
                else:
                    return 0.6
            else:
                return 0.8  # Flexible for other job types
                
        except Exception as e:
            logger.error(f"Error calculating availability match: {str(e)}")
            return 0.5
    
    def _get_match_level(self, score: float) -> str:
        """Get match level based on score"""
        if score >= 0.9:
            return "Excellent"
        elif score >= 0.8:
            return "Very Good"
        elif score >= 0.7:
            return "Good"
        elif score >= 0.6:
            return "Fair"
        elif score >= 0.5:
            return "Average"
        else:
            return "Poor"
    
    async def _generate_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if scores.get('skills_match', 0) < 0.7:
            recommendations.append("Consider additional training in required skills")
        
        if scores.get('experience_match', 0) < 0.6:
            recommendations.append("Gain more experience in the field")
        
        if scores.get('location_match', 0) < 0.5:
            recommendations.append("Consider relocation or remote work options")
        
        if scores.get('education_match', 0) < 0.8:
            recommendations.append("Consider pursuing additional education")
        
        if not recommendations:
            recommendations.append("Strong candidate profile")
        
        return recommendations
    
    async def find_top_matches(
        self, 
        job_data: Dict[str, Any], 
        candidates: List[Dict[str, Any]], 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Find top matching candidates for a job"""
        try:
            matches = []
            
            for candidate in candidates:
                match_result = await self.calculate_advanced_match_score(candidate, job_data)
                matches.append({
                    'candidate_id': candidate.get('id'),
                    'candidate_name': candidate.get('name'),
                    'match_score': match_result['total_score'],
                    'match_level': match_result['match_level'],
                    'detailed_scores': match_result['detailed_scores'],
                    'recommendations': match_result['recommendations']
                })
            
            # Sort by match score (descending)
            matches.sort(key=lambda x: x['match_score'], reverse=True)
            
            return matches[:limit]
            
        except Exception as e:
            logger.error(f"Error finding top matches: {str(e)}")
            raise

# Global instance
advanced_matching_service = AdvancedMatchingService() 