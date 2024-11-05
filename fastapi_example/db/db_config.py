from tortoise import Tortoise, run_async
import os
from functools import partial

from tortoise.contrib.fastapi import RegisterTortoise

DB_CONFIG = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": "localhost",
                "port": "8080",
                "user": "postgres",
                "password": "postgres",
                "database": "postgres",
                "min_size": 1,  # 최소 연결 수
                "max_size": 100,  # 최대 연결 수
                "ssl": False,  # SSL 사용 여부
                "timeout": 60,  # 연결 타임아웃
            }
        }
    },
    # 내가 등록할 앱네임들 지정
    "apps": {
        # app 프로젝트 이름 지정
        "my_app": {
            # models 가 정의된 app 내의 경로
            "models": ["apps.my_app.models"],  # 모델이 정의된 경로
            "default_connection": "default",
        },
        'blogs': {
            "models": ["apps.blogs.models"],
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 타임존 사용 여부
    "timezone": "UTC"  # 타임존 설정 (use_tz가 True일 경우 유효)
}


async def init():
    await Tortoise.init(DB_CONFIG)
    await Tortoise.generate_schemas()


# run_async(init())

register_orm = partial(
    RegisterTortoise,
    db_url=os.getenv("DB_URL", "sqlite://db.sqlite3"),
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
