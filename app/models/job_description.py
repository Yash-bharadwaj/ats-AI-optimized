from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class JobStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"

class JobType(str, Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    FREELANCE = "freelance"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class JobCreateRequest(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID for multi-tenancy")
    job_title: str = Field(..., description="Job title")
    company_name: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    job_type: JobType = Field(..., description="Type of job")
    job_status: JobStatus = Field(default=JobStatus.DRAFT, description="Job status")
    priority: Priority = Field(default=Priority.MEDIUM, description="Job priority")
    
    # Detailed job information
    description: Optional[str] = Field(None, description="Job description")
    requirements: Optional[List[str]] = Field(None, description="Job requirements")
    responsibilities: Optional[List[str]] = Field(None, description="Job responsibilities")
    skills: Optional[List[str]] = Field(None, description="Required skills")
    
    # Additional fields
    salary_range: Optional[Dict[str, Any]] = Field(None, description="Salary range")
    experience_level: Optional[str] = Field(None, description="Experience level")
    education_level: Optional[str] = Field(None, description="Education level")
    industry: Optional[str] = Field(None, description="Industry")
    department: Optional[str] = Field(None, description="Department")
    
    # Contact information
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    
    # Metadata
    tags: Optional[List[str]] = Field(None, description="Job tags")
    benefits: Optional[List[str]] = Field(None, description="Job benefits")
    
    # Location details
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    remote_work: Optional[bool] = Field(False, description="Remote work option")
    
    # Customer/Client information
    customer: Optional[str] = Field(None, description="Customer/Client name")
    
    class Config:
        use_enum_values = True

class JobResponse(BaseModel):
    job_id: str = Field(..., description="Unique job ID")
    tenant_id: str = Field(..., description="Tenant ID")
    job_title: str = Field(..., description="Job title")
    company_name: str = Field(..., description="Company name")
    location: str = Field(..., description="Job location")
    job_type: JobType = Field(..., description="Type of job")
    job_status: JobStatus = Field(..., description="Job status")
    priority: Priority = Field(..., description="Job priority")
    
    # Detailed job information
    description: Optional[str] = Field(None, description="Job description")
    requirements: Optional[List[str]] = Field(None, description="Job requirements")
    responsibilities: Optional[List[str]] = Field(None, description="Job responsibilities")
    skills: Optional[List[str]] = Field(None, description="Required skills")
    
    # Additional fields
    salary_range: Optional[Dict[str, Any]] = Field(None, description="Salary range")
    experience_level: Optional[str] = Field(None, description="Experience level")
    education_level: Optional[str] = Field(None, description="Education level")
    industry: Optional[str] = Field(None, description="Industry")
    department: Optional[str] = Field(None, description="Department")
    
    # Contact information
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    
    # Metadata
    tags: Optional[List[str]] = Field(None, description="Job tags")
    benefits: Optional[List[str]] = Field(None, description="Job benefits")
    
    # Location details
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State")
    country: Optional[str] = Field(None, description="Country")
    remote_work: Optional[bool] = Field(False, description="Remote work option")
    
    # Customer/Client information
    customer: Optional[str] = Field(None, description="Customer/Client name")
    
    # Timestamps
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    # AI-generated content
    ai_summary: Optional[str] = Field(None, description="AI-generated job summary")
    enhanced_description: Optional[str] = Field(None, description="AI-enhanced description")
    skill_analysis: Optional[Dict[str, Any]] = Field(None, description="AI skill analysis")
    
    class Config:
        use_enum_values = True

class JobListResponse(BaseModel):
    jobs: List[JobResponse] = Field(..., description="List of jobs")
    total_count: int = Field(..., description="Total number of jobs")
    limit: int = Field(..., description="Number of jobs per page")
    offset: int = Field(..., description="Offset for pagination")
    has_more: bool = Field(..., description="Whether there are more jobs")

class JobDescriptionParseRequest(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID")
    job_description: str = Field(..., description="Job description text")
    job_title: Optional[str] = Field(None, description="Job title")
    company_name: Optional[str] = Field(None, description="Company name")

class JobDescriptionResponse(BaseModel):
    tenant_id: str = Field(..., description="Tenant ID")
    job_title: str = Field(..., description="Extracted job title")
    company_name: Optional[str] = Field(None, description="Extracted company name")
    location: Optional[str] = Field(None, description="Extracted location")
    job_type: Optional[JobType] = Field(None, description="Extracted job type")
    description: str = Field(..., description="Enhanced job description")
    requirements: List[str] = Field(..., description="Extracted requirements")
    responsibilities: List[str] = Field(..., description="Extracted responsibilities")
    skills: List[str] = Field(..., description="Extracted skills")
    experience_level: Optional[str] = Field(None, description="Extracted experience level")
    education_level: Optional[str] = Field(None, description="Extracted education level")
    salary_range: Optional[Dict[str, Any]] = Field(None, description="Extracted salary range")
    benefits: List[str] = Field(..., description="Extracted benefits")
    industry: Optional[str] = Field(None, description="Extracted industry")
    department: Optional[str] = Field(None, description="Extracted department")
    tags: List[str] = Field(..., description="Generated tags")
    ai_summary: str = Field(..., description="AI-generated summary")
    skill_analysis: Dict[str, Any] = Field(..., description="Skill analysis")
    
    class Config:
        use_enum_values = True 