"""Databse Functionalities"""

from typing import Any, Dict, List, Tuple, Union

import psycopg2
from psycopg2._psycopg import cursor

from ..constant import (
    POSTGRES_DB,
    POSTGRES_DB_HOST,
    POSTGRES_DB_PORT,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
)
from ..logger import LOGGER


class PostgresSingletonConn:
    """Singleton implementation of postgres connection"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            # Initialize psycopg2 connection here
            cls._instance = psycopg2.connect(
                host=POSTGRES_DB_HOST,
                port=POSTGRES_DB_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
            )

        return cls._instance

    def get_connection(self) -> cursor:
        return self._instance


def init_database():
    LOGGER.info("Initializing database...")
    # Read the schema file
    with open("/app/schema.sql", "r", encoding="utf8") as sql_file:
        sql_script = sql_file.read()
    conn = PostgresSingletonConn()
    cursor = conn.cursor()

    cursor.execute(sql_script)
    conn.commit()

    LOGGER.info("Database successfully initialized.")
