from sqlalchemy.orm import DeclarativeMeta, sessionmaker, DeclarativeBase, declarative_base
from sqlalchemy import Column, String, Integer, UUID, DateTime, MetaData, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
import uuid
import asyncio

Base = declarative_base()

db_url = "postgresql+asyncpg://postgres:postgres@localhost:8080/postgres"
engine = create_async_engine(db_url, echo=True, execution_options={"isolation_level": "SERIALIZABLE"})
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


async def transaction_error_case_add_user(name, full_name):
    global session

    async with session() as session:
        # await session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
        # Transaction 시작
        async with session.begin() as _transaction:
            conn = await session.connection()
            print("현재 Transaction Level :", await conn.get_isolation_level())
            # await conn.connection(execution_options={"isolation_level": "SERIALIZABLE"})
            try:
                print(_transaction.is_active)
                new_user = User(name=name, full_name=full_name)
                session.add(new_user)
                raise ValueError("Trasaction Error")
                await session.commit()
            except Exception as e:
                print(e)
                await session.rollback()
            print(_transaction.is_active)
            return new_user


async def transaction_error_case_with_engine_repeatable_read(name, full_name, isolation_level="REPEATABLE READ"):
    global engine, session
    async with engine.connect() as conn:
        await conn.execution_options(isolation_level=f"{isolation_level}")
        print("현재 Transaction Level:", await conn.get_isolation_level())
        async with AsyncSession(bind=conn) as _session:  # 세션에 연결 바인딩
            # Transaction 시작
            async with _session.begin() as _transaction:
                print("REPEATABLE READ TRANSACTION ", _transaction.is_active)
                try:
                    new_user = User(name=name, full_name=full_name)
                    _session.add(new_user)
                    raise ValueError("Trasaction Error")
                    await _session.commit()
                except Exception as e:
                    print(e)
                    await _session.rollback()
                # 트랜잭션 종료
                print("REPEATABLE READ TRANSACTION ", _transaction.is_active)
                return new_user


async def transaction_with_save_point(name, full_name):
    global session
    async with session() as session:
        async with session.begin() as conn:

            try:
                new_user = User(name=name, full_name=full_name)
                result = await conn.query(User).filter(User.full_name == full_name).one()
                conn.begin_nested()  # save point
            except Exception as e:
                print(e)
                await conn.rollback()


async def main():
    await create_tables()  # 테이블 생성
    # 새 사용자 추가
    user = await transaction_error_case_add_user("Alice", "Alice Wonderland")
    user = await transaction_error_case_with_engine_repeatable_read(name="Alice", full_name="Alice Wonderland")
    # isolation_level = "REPEATABLE READ")
    print(f"Added user with ID: {user.id}, UUID: {user.uuid}, Created at: {user.created_at}")


asyncio.run(main())
