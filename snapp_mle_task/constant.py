"""Environment variables."""

import os

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_DB_HOST = os.getenv("POSTGRES_DB_HOST")
POSTGRES_DB_PORT = int(os.getenv("POSTGRES_DB_PORT"))
