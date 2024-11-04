# pylint: disable=E0611,E0401
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from db.db_config import DB_CONFIG, init
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


async def life_span(app: FastAPI):
    yield


app = FastAPI(title="Tortoise ORM FastAPI example", lifespan=life_span)
register_tortoise(app=app, config=DB_CONFIG, generate_schemas=True, add_exception_handlers=True)


# app.include_router(users_router, prefix="")


@app.get("/")
async def root():
    return {"Hello": "World"}
