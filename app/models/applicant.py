from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class ApplicantStatus(str, Enum):
    NEW = "new"
    REVIEWING = "reviewing"
    INTERVIEWING = "interviewing"
    HIRED = "hired"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class ApplicantSource(str, Enum):
    WEBSITE = "website"
    JOB_BOARD = "job_board"
    REFERRAL = "referral"
    RECRUITER = "recruiter"
    SOCIAL_MEDIA = "social_media"
    OTHER = "other"

class ApplicantCreateRequest(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID for multi-tenancy")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    
    # Personal information
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    nationality: Optional[str] = Field(None, description="Nationality")
    
    # Address information
    address: Optional[str] = Field(None, description="Address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    postal_code: Optional[str] = Field(None, description="Postal code")
    
    # Professional information
    current_position: Optional[str] = Field(None, description="Current position")
    current_company: Optional[str] = Field(None, description="Current company")
    years_of_experience: Optional[float] = Field(None, description="Years of experience")
    education_level: Optional[str] = Field(None, description="Education level")
    skills: Optional[List[str]] = Field(None, description="Skills")
    
    # Application information
    applicant_status: ApplicantStatus = Field(default=ApplicantStatus.NEW, description="Applicant status")
    applicant_source: ApplicantSource = Field(default=ApplicantSource.WEBSITE, description="Source of application")
    is_employee: bool = Field(default=False, description="Whether applicant is current employee")
    
    # Resume information
    resume_text: Optional[str] = Field(None, description="Resume text content")
    resume_file_path: Optional[str] = Field(None, description="Resume file path")
    resume_file_name: Optional[str] = Field(None, description="Resume file name")
    
    # Additional information
    linkedin_url: Optional[str] = Field(None, description="LinkedIn URL")
    portfolio_url: Optional[str] = Field(None, description="Portfolio URL")
    github_url: Optional[str] = Field(None, description="GitHub URL")
    notes: Optional[str] = Field(None, description="Notes about the applicant")
    
    # Metadata
    tags: Optional[List[str]] = Field(None, description="Tags for the applicant")
    salary_expectation: Optional[Dict[str, Any]] = Field(None, description="Salary expectation")
    availability: Optional[str] = Field(None, description="Availability")
    preferred_work_type: Optional[str] = Field(None, description="Preferred work type")
    
    class Config:
        use_enum_values = True

class ApplicantUpdateRequest(BaseModel):
    first_name: Optional[str] = Field(None, description="First name")
    last_name: Optional[str] = Field(None, description="Last name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    
    # Personal information
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    nationality: Optional[str] = Field(None, description="Nationality")
    
    # Address information
    address: Optional[str] = Field(None, description="Address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    postal_code: Optional[str] = Field(None, description="Postal code")
    
    # Professional information
    current_position: Optional[str] = Field(None, description="Current position")
    current_company: Optional[str] = Field(None, description="Current company")
    years_of_experience: Optional[float] = Field(None, description="Years of experience")
    education_level: Optional[str] = Field(None, description="Education level")
    skills: Optional[List[str]] = Field(None, description="Skills")
    
    # Application information
    applicant_status: Optional[ApplicantStatus] = Field(None, description="Applicant status")
    applicant_source: Optional[ApplicantSource] = Field(None, description="Source of application")
    is_employee: Optional[bool] = Field(None, description="Whether applicant is current employee")
    
    # Resume information
    resume_text: Optional[str] = Field(None, description="Resume text content")
    resume_file_path: Optional[str] = Field(None, description="Resume file path")
    resume_file_name: Optional[str] = Field(None, description="Resume file name")
    
    # Additional information
    linkedin_url: Optional[str] = Field(None, description="LinkedIn URL")
    portfolio_url: Optional[str] = Field(None, description="Portfolio URL")
    github_url: Optional[str] = Field(None, description="GitHub URL")
    notes: Optional[str] = Field(None, description="Notes about the applicant")
    
    # Metadata
    tags: Optional[List[str]] = Field(None, description="Tags for the applicant")
    salary_expectation: Optional[Dict[str, Any]] = Field(None, description="Salary expectation")
    availability: Optional[str] = Field(None, description="Availability")
    preferred_work_type: Optional[str] = Field(None, description="Preferred work type")
    
    class Config:
        use_enum_values = True

class ApplicantResponse(BaseModel):
    applicant_id: str = Field(..., description="Unique applicant ID")
    tenant_id: str = Field(..., description="Tenant ID")
    first_name: str = Field(..., description="First name")
    last_name: str = Field(..., description="Last name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    
    # Personal information
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender")
    nationality: Optional[str] = Field(None, description="Nationality")
    
    # Address information
    address: Optional[str] = Field(None, description="Address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    postal_code: Optional[str] = Field(None, description="Postal code")
    
    # Professional information
    current_position: Optional[str] = Field(None, description="Current position")
    current_company: Optional[str] = Field(None, description="Current company")
    years_of_experience: Optional[float] = Field(None, description="Years of experience")
    education_level: Optional[str] = Field(None, description="Education level")
    skills: Optional[List[str]] = Field(None, description="Skills")
    
    # Application information
    applicant_status: ApplicantStatus = Field(..., description="Applicant status")
    applicant_source: ApplicantSource = Field(..., description="Source of application")
    is_employee: bool = Field(..., description="Whether applicant is current employee")
    
    # Resume information
    resume_text: Optional[str] = Field(None, description="Resume text content")
    resume_file_path: Optional[str] = Field(None, description="Resume file path")
    resume_file_name: Optional[str] = Field(None, description="Resume file name")
    
    # Additional information
    linkedin_url: Optional[str] = Field(None, description="LinkedIn URL")
    portfolio_url: Optional[str] = Field(None, description="Portfolio URL")
    github_url: Optional[str] = Field(None, description="GitHub URL")
    notes: Optional[str] = Field(None, description="Notes about the applicant")
    
    # Metadata
    tags: Optional[List[str]] = Field(None, description="Tags for the applicant")
    salary_expectation: Optional[Dict[str, Any]] = Field(None, description="Salary expectation")
    availability: Optional[str] = Field(None, description="Availability")
    preferred_work_type: Optional[str] = Field(None, description="Preferred work type")
    
    # Timestamps
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    created_by: str = Field(..., description="User who created the applicant")
    updated_by: str = Field(..., description="User who last updated the applicant")
    
    # AI-generated content
    ai_summary: Optional[str] = Field(None, description="AI-generated summary")
    skill_analysis: Optional[Dict[str, Any]] = Field(None, description="AI skill analysis")
    experience_analysis: Optional[Dict[str, Any]] = Field(None, description="AI experience analysis")
    
    class Config:
        use_enum_values = True

class ApplicantListResponse(BaseModel):
    applicants: List[ApplicantResponse] = Field(..., description="List of applicants")
    total_count: int = Field(..., description="Total number of applicants")
    limit: int = Field(..., description="Number of applicants per page")
    offset: int = Field(..., description="Offset for pagination")
    has_more: bool = Field(..., description="Whether there are more applicants")

class ApplicantSearchRequest(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID")
    query: str = Field(..., description="Search query")
    filters: Optional[Dict[str, Any]] = Field(None, description="Search filters")
    limit: int = Field(10, ge=1, le=100, description="Number of results to return")
    offset: int = Field(0, ge=0, description="Offset for pagination")
    min_similarity: float = Field(0.0, ge=0.0, le=1.0, description="Minimum similarity score")

class ApplicantAnalytics(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID")
    total_applicants: int = Field(..., description="Total number of applicants")
    applicants_by_status: Dict[str, int] = Field(..., description="Applicants grouped by status")
    applicants_by_source: Dict[str, int] = Field(..., description="Applicants grouped by source")
    applicants_by_location: Dict[str, int] = Field(..., description="Applicants grouped by location")
    average_experience: Optional[float] = Field(None, description="Average years of experience")
    top_skills: List[Dict[str, Any]] = Field(..., description="Most common skills")
    recent_applications: int = Field(..., description="Applications in last 30 days")
    conversion_rate: Optional[float] = Field(None, description="Application to hire conversion rate")

# Legacy models for backward compatibility
class ResumeResponse(BaseModel):
    resume_id: str = Field(..., description="Resume ID")
    tenant_id: str = Field(..., description="Tenant ID")
    candidate_name: str = Field(..., description="Candidate name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    resume_text: str = Field(..., description="Resume text content")
    skills: List[str] = Field(..., description="Extracted skills")
    experience: Optional[str] = Field(None, description="Experience summary")
    education: Optional[str] = Field(None, description="Education summary")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

class ResumeListResponse(BaseModel):
    resumes: List[ResumeResponse] = Field(..., description="List of resumes")
    total_count: int = Field(..., description="Total number of resumes")
    limit: int = Field(..., description="Number of resumes per page")
    offset: int = Field(..., description="Offset for pagination")
    has_more: bool = Field(..., description="Whether there are more resumes") 