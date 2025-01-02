from fastapi import APIRouter
from apis.routes.tournaments import tournament_router
from apis.routes.blogs import blogs_router
from apis.routes.lottos import lotto_router
from apis.routes.trades import trades_router

api_router = APIRouter()

api_router.include_router(tournament_router, prefix="/tournaments", tags=["tournaments"])
api_router.include_router(blogs_router, prefix="/blog", tags=["blog"])
api_router.include_router(lotto_router, prefix="/lotto", tags=["lotto"])
api_router.include_router(trades_router, prefix="/trades", tags=["trades"])
