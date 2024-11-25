from fastapi import APIRouter
from apis.routes.tournaments import tournament_router
from apis.routes.blogs import blogs_router

api_router = APIRouter()

api_router.include_router(tournament_router, prefix="/tournaments", tags=["tournaments"])
api_router.include_router(blogs_router, prefix="/blog", tags=["blog"])