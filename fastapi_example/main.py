# pylint: disable=E0611,E0401
import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi_example.db.db_config import DB_CONFIG, init
from fastapi import FastAPI
from tortoise import Tortoise, generate_config
from tortoise.contrib.fastapi import register_tortoise, RegisterTortoise


@asynccontextmanager
async def lifespan_test(app: FastAPI) -> AsyncGenerator[None, None]:
    config = generate_config(
        os.getenv("TORTOISE_TEST_DB", "sqlite://:memory:"),
        app_modules={
                "my_app": ["fastapi_example.apps.my_app.models"]},
        testing=True,
        connection_label="default",
    )
    async with RegisterTortoise(
            app=app,
            config=config,
            generate_schemas=True,
            add_exception_handlers=True,
            _create_db=True,
    ):
        # db connected
        yield
        # app teardown
    # db connections closed
    await Tortoise.close_connections()
    #await Tortoise._drop_databases()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    if getattr(app.state, "testing", None):
        async with lifespan_test(app) as _:
            yield
    else:
        # app startup
        async with RegisterTortoise(
                app=app,
                config=DB_CONFIG,
                generate_schemas=True,
                add_exception_handlers=True
        ):
            yield


app = FastAPI(title="Tortoise ORM FastAPI example", lifespan=lifespan)


# app.include_router(users_router, prefix="")


@app.get("/")
async def root():
    return {"Hello": "World"}
