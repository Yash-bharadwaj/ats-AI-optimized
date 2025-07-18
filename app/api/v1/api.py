from fastapi import APIRouter

api_router = APIRouter()

# Only include Railway-optimized endpoints to avoid import issues
try:
    from app.api.v1.endpoints import railway_resume
    api_router.include_router(railway_resume.router, prefix="/railway", tags=["railway"])
except Exception as e:
    # Create fallback endpoints if import fails
    @api_router.get("/railway/health/railway")
    async def railway_health_fallback():
        return {
            "status": "degraded",
            "message": "Railway endpoints not available",
            "railway_mode": True
        }
