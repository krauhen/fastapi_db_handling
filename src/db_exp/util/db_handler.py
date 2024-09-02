import asyncpg
from db_exp.models.db import DBParams
from asyncpg import Connection


async def get_db(db_params: DBParams) -> Connection:
    try:
        conn: Connection = await asyncpg.connect(**db_params.dict())
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None


async def create_database(db_params: DBParams):
    try:
        default_db_params = DBParams(
            database="postgres",
            user=db_params.user,
            password=db_params.password,
            host=db_params.host,
            port=db_params.port,
        )
        conn = await get_db(default_db_params)
        if conn is None:
            return

        async with conn.transaction():
            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1", db_params.database
            )

            if not exists:
                await conn.execute(
                    f"CREATE DATABASE {db_params.database}"
                )
                print(f"Database '{db_params.database}' created successfully.")
            else:
                print(f"Database '{db_params.database}' already exists.")

        await conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")


async def create_tables(db_params: DBParams):
    try:
        conn = await get_db(db_params)
        if conn is None:
            return

        async with conn.transaction():
            create_table_queries = [
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS images (
                    image_id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    image_url TEXT NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    metadata_id SERIAL PRIMARY KEY,
                    image_id INTEGER NOT NULL,
                    key VARCHAR(50) NOT NULL,
                    value TEXT NOT NULL,
                    FOREIGN KEY (image_id) REFERENCES images (image_id) ON DELETE CASCADE
                )
                """,
            ]

            for query in create_table_queries:
                await conn.execute(query)
                print("Table created or already exists.")

        await conn.close()
    except Exception as e:
        print(f"Error creating tables: {e}")
