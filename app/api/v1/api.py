from fastapi import APIRouter
from app.api.v1.endpoints import resume, job_description, jobs, applicants, advanced_resume, railway_resume

api_router = APIRouter()

api_router.include_router(resume.router, prefix="/resume", tags=["resume"])
api_router.include_router(job_description.router, prefix="/job-description", tags=["job-description"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(applicants.router, prefix="/applicants", tags=["applicants"])
api_router.include_router(advanced_resume.router, prefix="/advanced", tags=["advanced"])
api_router.include_router(railway_resume.router, prefix="/railway", tags=["railway"])
