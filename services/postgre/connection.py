from src.secret import Config
from sqlalchemy.sql import text
from src.exceptions import ServicesConnectionError
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

config = Config()

engine: AsyncEngine | None = None


async def database_connection() -> AsyncEngine:
    global engine
    if not engine:
        try:
            engine = create_async_engine(
                url=config.PGSQL_CONNECTION, pool_pre_ping=True
            )
            async with engine.connect() as connection:
                await connection.execute(text("SELECT 1"))

        except ConnectionRefusedError:
            raise ServicesConnectionError(
                detail="Please ensure your database server is turned on!",
                name="PostgreSQL",
            )

    return engine


async def close_database_connection():
    global engine
    if engine:
        await engine.dispose()
        engine = None
