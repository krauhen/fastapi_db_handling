import psycopg
from psycopg import sql, OperationalError


database_manager = None


class DatabaseManager:
    def __init__(self):
        self.db_default_params = None

    @staticmethod
    def get_database_manager():
        global database_manager
        if database_manager is None:
            database_manager = DatabaseManager()
        return database_manager

    def set_db_default_params(self, db_params):
        self.db_default_params = db_params

    def get_connection(self):
        return psycopg.connect(**self.db_default_params.dict())

    def create_database(self, database_name):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s"),
                        [database_name]
                    )
                    exists = cursor.fetchone()
                    if not exists:
                        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database_name)))
                        print(f"Database '{database_name}' created.")
                    else:
                        print(f"Database '{database_name}' already exists.")
        except OperationalError as e:
            raise e

    def create_table(self, table_name):
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        sql.SQL("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s);"),
                        [table_name]
                    )
                    exists = cursor.fetchone()[0]
                    if not exists:
                        cursor.execute(sql.SQL("""
                            CREATE TABLE {} (
                                id SERIAL PRIMARY KEY,
                                name VARCHAR(100) NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            );
                        """).format(sql.Identifier(table_name)))
                        print(f"Table '{table_name}' created.")
                    else:
                        print(f"Table '{table_name}' already exists.")
        except OperationalError as e:
            raise e
