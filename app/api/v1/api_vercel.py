from fastapi import APIRouter

from app.api.v1.endpoints import resume_vercel, job_description

api_router = APIRouter()

# Core parsing endpoints (Vercel-optimized)
api_router.include_router(resume_vercel.router, prefix="/resume", tags=["resume"])
api_router.include_router(job_description.router, prefix="/job", tags=["job-description"])

# Note: Removed jobs and applicants endpoints for Vercel deployment
# to reduce bundle size and complexity 