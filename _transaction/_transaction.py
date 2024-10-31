from sqlalchemy.orm import DeclarativeMeta, sessionmaker, DeclarativeBase, declarative_base
from sqlalchemy import Column, String, Integer, UUID, DateTime, MetaData, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import uuid
import asyncio

Base = declarative_base()

db_url = "postgresql+asyncpg://postgres:postgres@localhost:8080/postgres"
engine = create_async_engine(db_url, echo=True)
session = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    full_name = Column(String)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())


async def add_user(name, full_name):
    global session
    async with session() as session:
        async with session.begin():
            new_user = User(name=name, full_name=full_name)
            session.add(new_user)
            await session.commit()
        return new_user


async def main():
    await create_tables()  # 테이블 생성
    # 새 사용자 추가
    user = await add_user("Alice", "Alice Wonderland")
    print(f"Added user with ID: {user.id}, UUID: {user.uuid}, Created at: {user.created_at}")


asyncio.run(main())
