import asyncpg


DB_POOL = None


async def connect_postgres():
    global DB_POOL
    if DB_POOL is None:
        DB_POOL = await asyncpg.create_pool(
            user="testchaos",            # PostgreSQL username
            password="chaos007",              # PostgreSQL password
            database="testchaosbotDB",             # Название базы данных
            host="localhost",                   # Или IP / render.com URL
            port=5432                           # Стандартный порт PostgreSQL
        )


async def fetchrow(query, *args):
    async with DB_POOL.acquire() as conn:
        return await conn.fetchrow(query, *args)
