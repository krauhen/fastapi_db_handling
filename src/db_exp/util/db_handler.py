import psycopg2
import asyncpg

from psycopg2 import sql
from db_exp.models.db import DBParams


async def get_db():
    global db_params
    conn = await asyncpg.connect(
        user=db_params.user,
        password=db_params.password,
        database=db_params.dbname,
        host=db_params.host,
        port=db_params.port,
    )
    try:
        yield conn
    finally:
        await conn.close()


def create_database(db_params: DBParams):
    try:
        default_db_params = DBParams(
            user=db_params.user,
            password=db_params.password,
            host=db_params.host,
            port=db_params.port,
        )
        conn = psycopg2.connect(**default_db_params.dict())
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_params.dbname,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_params.dbname))
            )
            print(f"Database '{db_params.dbname}' created successfully.")
        else:
            print(f"Database '{db_params.dbname}' already exists.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")


def create_tables(db_params: DBParams):
    try:
        conn = psycopg2.connect(**db_params.dict())
        cur = conn.cursor()

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
            cur.execute(query)
            print("Table created or already exists.")

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error creating tables: {e}")
