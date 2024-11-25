from fastapi import APIRouter, Depends, Request
from typing import List

from starlette import status

from apps.my_app.models import Tournament
from apps.my_app.schema import Tournament_Pydantic, Tournament_PydanticList
from tortoise.transactions import in_transaction, atomic
from random import randint

tournament_router = APIRouter()


@tournament_router.get("/search/{name}", response_model=List[Tournament_Pydantic])
async def search_tournaments(request: Request, name: str):
    matched_tournaments = await Tournament.filter(name=name)
    # print(await Tournament_PydanticList.from_queryset(matched_tournaments))
    return matched_tournaments


@tournament_router.post("/", response_model=Tournament_Pydantic,status_code=status.HTTP_201_CREATED)
@atomic()
async def save_tournament(request: Request, tournament: Tournament_Pydantic):
    tournament_model = await Tournament.create(**tournament.dict())
    return tournament.dict()
