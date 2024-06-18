"""Databse Functionalities"""

from typing import Any, Dict, List, Tuple, Union

import os

from sqlalchemy import create_engine


class MySQLConn:
    """Connecting to mysql."""

    def __init__(self):
        """Instantiating connection."""
        self.db_engine = create_engine(
            "mysql://{username}:{password}@{host}:{port}/{db}?charset={ch}".format(
                username=os.getenv("MYSQL_USER"),
                password=os.getenv("MYSQL_PASSWORD"),
                host=os.getenv("ASM_API_MYSQL_HOST"),
                port=os.getenv("ASM_API_MYSQL_PORT"),
                db=os.getenv("ASM_API_TAG_SYS_DB"),
                ch="utf8",
            )
        )

    def __enter__(self):
        """conncect to database."""
        self.conn = self.db_engine.connect()
        return self.conn

    def __exit__(self, exc_type, exc_value, tb):
        self.conn.close()
        self.db_engine.dispose()
        if exc_type is not None:
            raise Exception(exc_type)
        return True
