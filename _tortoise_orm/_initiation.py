from tortoise import Tortoise, run_async

# db_url = "postgresql+asyncpg://postgres:postgres@localhost:8080/postgres"
#
#
# async def init():
#     # Here we create a SQLite DB using file "db.sqlite3"
#     #  also specify the app name of "models"
#     #  which contain models from "app.models"
#     await Tortoise.init(
#         db_url="postgres://username:password@localhost:5432/database_name",
#         modules={"models": ["_tortoise_orm._models"]}
#     )
#     # Generate the schema
#     await Tortoise.generate_schemas()
#
#
# run_async(init())

POSTGRES_CONFIG = {
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
    # 내가 등록팔 앱네임들 지정
    "apps": {
        # app 프로젝트 이름 지정
        "app": {
            # models 가 정의된 app 내의 경로
            "models": ["app._models"],  # 모델이 정의된 경로
            "default_connection": "default",
        }
    },
    "use_tz": False,  # 타임존 사용 여부
    "timezone": "UTC"  # 타임존 설정 (use_tz가 True일 경우 유효)
}


async def init():
    await Tortoise.init(POSTGRES_CONFIG)
    await Tortoise.generate_schemas()


run_async(init())
