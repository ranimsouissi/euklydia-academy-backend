from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, assessment
from app.api.v1.endpoints import career_paths
from app.api.v1.endpoints import brochure
from app.api.v1.endpoints import users
from app.api.v1.endpoints import roadmap
from app.api.v1.endpoints import modules
from app.api.v1.endpoints import upload
from app.api.v1.endpoints import learning_content  # ✅ nouveau
from app.api.v1.endpoints import lessons           # ✅ nouveau

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["assessment"])
api_router.include_router(career_paths.router, prefix="/career-paths", tags=["career-paths"])
api_router.include_router(brochure.router)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(roadmap.router, prefix="/roadmap", tags=["roadmap"])
api_router.include_router(modules.router, prefix="/modules", tags=["modules"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(learning_content.router, tags=["learning-content"])  # ✅ nouveau
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])  # ✅ nouveau