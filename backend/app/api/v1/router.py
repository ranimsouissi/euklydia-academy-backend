# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import health, auth, diagnostic
from app.api.v1.endpoints import career_paths
from app.api.v1.endpoints import users
from app.api.v1.endpoints import roadmap
from app.api.v1.endpoints import modules
from app.api.v1.endpoints import upload
from app.api.v1.endpoints import coaching
from app.api.v1.endpoints import performance
from app.api.v1.endpoints import admin
from app.api.v1.endpoints import recommendation
from app.api.v1.endpoints import analytics
from app.api.v1.endpoints import kpi

api_router = APIRouter()
api_router.include_router(health.router,            tags=["health"])
api_router.include_router(auth.router,              prefix="/auth",         tags=["auth"])
api_router.include_router(diagnostic.router,        prefix="/diagnostic",   tags=["diagnostic"])
api_router.include_router(career_paths.router,      prefix="/career-paths", tags=["career-paths"])
api_router.include_router(users.router,             prefix="/users",        tags=["users"])
api_router.include_router(roadmap.router,           prefix="/roadmap",      tags=["roadmap"])
api_router.include_router(modules.router,           prefix="/modules",      tags=["modules"])
api_router.include_router(upload.router,            prefix="/upload",       tags=["upload"])
api_router.include_router(coaching.router,          prefix="/coaching",     tags=["coaching"])
api_router.include_router(performance.router,       prefix="/performance",  tags=["performance"])
api_router.include_router(admin.router,             prefix="/admin",        tags=["admin"])
api_router.include_router(recommendation.router,  prefix="/recommendation", tags=["recommendation"])
api_router.include_router(analytics.router,        prefix="/analytics",      tags=["analytics"])
api_router.include_router(kpi.router, prefix="/kpi", tags=["kpi"])
