from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import asyncio
from sqlalchemy import text

DB_URL = "sqlite+aiosqlite:///./mydb.db"

async_engine = create_async_engine(DB_URL)

AsyncSessionLocal = async_sessionmaker(bind=async_engine, autoflush=False, autocommit=False)


async def get_db_session():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()

#Connection tester function:
# async def check():
#     async with async_engine.connect() as conn:
#         result = await conn.execute(text("SELECT 1"))
#         print("Connected! Result:", result.scalar())

# asyncio.run(check())



